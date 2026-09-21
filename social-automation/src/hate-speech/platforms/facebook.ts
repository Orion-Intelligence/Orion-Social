import { getSocialContext } from '../../session/session-manager.js';
import { trackContext, untrackContext } from '../../session/shutdown.js';
import { errorReason, isSessionExpired } from '../../shared/result-writer.js';
import type { HateSpeechMonitorResult } from '../model/models.js';
import type { BrowserContext } from 'playwright';
import { createEmptyHateSpeechMonitorResult } from '../constants/constants.js';
import { SocialAutomationError } from '../../shared/errors.js';

export class FacebookHateSpeechMonitor {
  private readonly platform = 'facebook';

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
      console.error('[FacebookHateSpeechMonitor] getSocialContext failed:', error);
      result.error = true;
      result.error_reason = errorReason(error);
      result.session_expired = isSessionExpired(error);
      return result;
    }

    trackContext(context);

    try {
      console.log(`[FacebookHateSpeechMonitor] Starting run for ${this.profileUrl}`);
      const page = context.pages()[0] ?? await context.newPage();
      console.log(`[FacebookHateSpeechMonitor] Navigating...`);
      await page.goto(this.profileUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
      console.log(`[FacebookHateSpeechMonitor] Navigated. Waiting for timeline...`);
      try {
        await page.waitForSelector('div[role="article"]', { timeout: 15000 });
      } catch {
        console.log(`[FacebookHateSpeechMonitor] Timeout waiting for posts, will proceed anyway.`);
      }

      if (page.url().includes('login') || (await page.locator('input[name="email"]').count()) > 0) {
        throw new SocialAutomationError('Session expired: Redirected to login page.', 'SESSION_EXPIRED');
      }

      console.log(`[FacebookHateSpeechMonitor] Wait done. Start scrolling...`);

      const extractedUrls = new Set<string>();
      let emptyScrolls = 0;

      while (result.posts.length < this.postCount && emptyScrolls < 10) {
        const items = page.locator('div[aria-posinset], div[role="article"], div[data-pagelet^="FeedUnit"]');
        const count = await items.count();
        let addedThisScroll = 0;
        console.log(`[FacebookHateSpeechMonitor] Found ${count} posts on screen. Empty scrolls: ${emptyScrolls}, Total extracted: ${result.posts.length}`);

        for (let j = 0; j < count; j++) {
          if (result.posts.length >= this.postCount) break;

          const item = items.nth(j);
          try {
            const links = await item.locator('a[href*="/posts/"], a[href*="/permalink/"], a[href*="story_fbid"], a[href*="l.facebook.com"], a[target="_blank"]').all();
            let postUrl = 'Unknown URL';
            for (const link of links) {
              const href = await link.getAttribute('href') || '';
              if (!href || href.startsWith('?') || href.startsWith('#')) continue;
              let candidate = href.startsWith('http') ? href : 'https://www.facebook.com' + href;
              if (candidate.includes('l.facebook.com')) {
                const target = new URL(candidate).searchParams.get('u') || '';
                if (!target.startsWith('http')) continue;
                candidate = target;
              }
              postUrl = candidate.split('?')[0];
              break;
            }

            if (postUrl !== 'Unknown URL' && !extractedUrls.has(postUrl)) {
              extractedUrls.add(postUrl);
              const textContent = await item.innerText();
              const lines = textContent.split('\n').map(l => l.trim()).filter(l => l.length > 0);

              const labels = ['Sponsored', '⁠'];
              const noise = [...labels, 'Facebook', '·', 'Online status indicator', 'Active'];
              const isAd = lines.some(line => labels.includes(line));
              if (isAd) continue;

              const headerLink = item.locator('h2 a, h3 a, h4 a, strong a').first();
              const header = await headerLink.innerText({ timeout: 1000 }).catch(() => '');
              const author = header.trim() || (lines.find(line => !noise.includes(line)) ?? 'Unknown');
              const content = lines.filter(line => !noise.includes(line) && line !== author);
              const contentText = content.slice(0, 4).join(' | ');

              const likesMatch = textContent.match(/([\d,.]+[KMB]?)\s+(likes?|upvotes?)/i);
              const viewsMatch = textContent.match(/([\d,.]+[KMB]?)\s+views?/i);

              result.posts.push({
                url: postUrl,
                author,
                content_text: contentText,
                likes: likesMatch ? likesMatch[1] : '0',
                shares: '',
                views: viewsMatch ? viewsMatch[1] : '0',
                detected_at: new Date().toISOString(),
              });
              addedThisScroll++;
            }
          } catch {}
        }

        if (addedThisScroll === 0) {
          emptyScrolls++;
          console.log(`[FacebookHateSpeechMonitor] Added 0 posts this scroll. Empty scrolls incremented to ${emptyScrolls}`);
        } else {
          emptyScrolls = 0;
          console.log(`[FacebookHateSpeechMonitor] Added ${addedThisScroll} posts this scroll. Reset empty scrolls.`);
        }

        if (result.posts.length < this.postCount) {
          console.log(`[FacebookHateSpeechMonitor] Scrolling down...`);
          await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
          await page.waitForTimeout(3000);
        }
      }

      result.total_posts = result.posts.length;
      console.log(`[FacebookHateSpeechMonitor] Run completed successfully with ${result.total_posts} posts.`);

    } catch (error) {
      console.error('[FacebookHateSpeechMonitor] Fatal error during run:', error);
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
