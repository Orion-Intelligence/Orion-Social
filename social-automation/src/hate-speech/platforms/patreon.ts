import { getSocialContext } from '../../session/session-manager.js';
import { trackContext, untrackContext } from '../../session/shutdown.js';
import { errorReason, isSessionExpired } from '../../shared/result-writer.js';
import type { HateSpeechMonitorResult } from '../model/models.js';
import type { BrowserContext } from 'playwright';
import { createEmptyHateSpeechMonitorResult } from '../constants/constants.js';
import { SocialAutomationError } from '../../shared/errors.js';

export class PatreonHateSpeechMonitor {
  private readonly platform = 'patreon';

  constructor(
    private readonly sessionFile: string | undefined,
    private readonly profileUrl: string,
    private readonly postCount: number
  ) {}

  async run(): Promise<HateSpeechMonitorResult> {
    const result = createEmptyHateSpeechMonitorResult();

    let context: BrowserContext;
    try {
      context = await getSocialContext(this.platform, 'default', this.sessionFile);
    } catch (error) {
      console.error('[PatreonHateSpeechMonitor] getSocialContext failed:', error);
      result.error = true;
      result.error_reason = errorReason(error);
      result.session_expired = isSessionExpired(error);
      return result;
    }

    trackContext(context);

    try {
      console.log(`[PatreonHateSpeechMonitor] Starting run for ${this.profileUrl}`);
      const page = context.pages()[0] ?? await context.newPage();
      console.log(`[PatreonHateSpeechMonitor] Navigating...`);
      await page.goto(this.profileUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
      console.log(`[PatreonHateSpeechMonitor] Navigated. Waiting for posts...`);
      try {
        await page.waitForSelector('[data-tag="post-card"]', { timeout: 15000 });
      } catch {
        console.log(`[PatreonHateSpeechMonitor] Timeout waiting for posts, will proceed anyway.`);
      }

      if (page.url().includes('login') || (await page.locator('input[type="password"]').count()) > 0) {
        throw new SocialAutomationError('Session expired: Redirected to login page.', 'SESSION_EXPIRED');
      }

      console.log(`[PatreonHateSpeechMonitor] Wait done. Start scrolling...`);

      const extractedUrls = new Set<string>();
      let emptyScrolls = 0;

      while (result.posts.length < this.postCount && emptyScrolls < 10) {
        const items = page.locator('[data-tag="post-card"]');
        const count = await items.count();
        let addedThisScroll = 0;
        console.log(`[PatreonHateSpeechMonitor] Found ${count} posts on screen. Empty scrolls: ${emptyScrolls}, Total extracted: ${result.posts.length}`);

        for (let j = 0; j < count; j++) {
          if (result.posts.length >= this.postCount) break;

          const item = items.nth(j);
          try {
            const links = await item.locator('a[href*="/posts/"]').all();
            let postUrl = 'Unknown URL';
            if (links.length > 0) {
              const href = await links[0].getAttribute('href') || '';
              postUrl = href.startsWith('http') ? href : 'https://www.patreon.com' + href;
              postUrl = postUrl.split('?')[0];
            }

            if (postUrl !== 'Unknown URL' && !extractedUrls.has(postUrl)) {
              extractedUrls.add(postUrl);
              const textContent = await item.innerText();
              const lines = textContent.split('\n').map(l => l.trim()).filter(l => l.length > 0);
              const author = lines.length > 0 ? lines[0] : 'Unknown';

              const isAd = lines.some(line => ['Sponsored', 'Promoted'].includes(line));
              if (isAd) continue;

              const contentText = lines.slice(1, 4).join(' | ');

              let likes = '0', shares = '', views = '0';
              try {
                const likesMatch = textContent.match(/([\d,.]+[KMB]?)\s+(likes?|upvotes?)/i);
                const viewsMatch = textContent.match(/([\d,.]+[KMB]?)\s+views?/i);
                if (likesMatch) likes = likesMatch[1];
                if (viewsMatch) views = viewsMatch[1];
              } catch {}

              result.posts.push({
                url: postUrl,
                author,
                content_text: contentText,
                likes,
                shares,
                views,
                detected_at: new Date().toISOString(),
              });
              addedThisScroll++;
            }
          } catch {
          }
        }

        if (addedThisScroll === 0) {
          emptyScrolls++;
          console.log(`[PatreonHateSpeechMonitor] Added 0 posts this scroll. Empty scrolls incremented to ${emptyScrolls}`);
        } else {
          emptyScrolls = 0;
          console.log(`[PatreonHateSpeechMonitor] Added ${addedThisScroll} posts this scroll. Reset empty scrolls.`);
        }

        if (result.posts.length < this.postCount) {
          console.log(`[PatreonHateSpeechMonitor] Scrolling down...`);
          await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
          await page.waitForTimeout(3000);
        }
      }

      result.total_posts = result.posts.length;
      console.log(`[PatreonHateSpeechMonitor] Run completed successfully with ${result.total_posts} posts.`);

    } catch (error) {
      console.error('[PatreonHateSpeechMonitor] Fatal error during run:', error);
      result.error = true;
      result.error_reason = errorReason(error);
      result.session_expired = isSessionExpired(error);
    } finally {
      untrackContext(context);
      await context.close();
    }

    return result;
  }
}
