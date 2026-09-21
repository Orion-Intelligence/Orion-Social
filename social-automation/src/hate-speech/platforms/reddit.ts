import { getSocialContext } from '../../session/session-manager.js';
import { trackContext, untrackContext } from '../../session/shutdown.js';
import { errorReason, isSessionExpired } from '../../shared/result-writer.js';
import type { HateSpeechMonitorResult } from '../model/models.js';
import type { BrowserContext } from 'playwright';
import { createEmptyHateSpeechMonitorResult } from '../constants/constants.js';
import { SocialAutomationError } from '../../shared/errors.js';

export class RedditHateSpeechMonitor {
  private readonly platform = 'reddit';

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
      console.error('[RedditHateSpeechMonitor] getSocialContext failed:', error);
      result.error = true;
      result.error_reason = errorReason(error);
      result.session_expired = isSessionExpired(error);
      return result;
    }

    trackContext(context);

    try {
      console.log(`[RedditHateSpeechMonitor] Starting run for ${this.profileUrl}`);
      const page = context.pages()[0] ?? await context.newPage();
      console.log(`[RedditHateSpeechMonitor] Navigating...`);
      await page.goto(this.profileUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
      console.log(`[RedditHateSpeechMonitor] Navigated. Waiting for timeline...`);
      try {
        await page.waitForSelector('shreddit-post', { timeout: 15000 });
      } catch {
        console.log(`[RedditHateSpeechMonitor] Timeout waiting for posts, will proceed anyway.`);
      }

      if (page.url().includes('login') || (await page.locator('input[name="username"]').count()) > 0) {
        throw new SocialAutomationError('Session expired: Redirected to login page.', 'SESSION_EXPIRED');
      }

      console.log(`[RedditHateSpeechMonitor] Wait done. Start scrolling...`);

      const extractedUrls = new Set<string>();
      let emptyScrolls = 0;

      while (result.posts.length < this.postCount && emptyScrolls < 10) {
        const items = page.locator('shreddit-post, shreddit-ad-post');
        const count = await items.count();
        let addedThisScroll = 0;
        console.log(`[RedditHateSpeechMonitor] Found ${count} posts on screen. Empty scrolls: ${emptyScrolls}, Total extracted: ${result.posts.length}`);

        for (let j = 0; j < count; j++) {
          if (result.posts.length >= this.postCount) break;

          const item = items.nth(j);
          try {
            const links = await item.locator('a[slot="full-post-link"], a[href*="/comments/"], a[href^="http"]').all();
            let postUrl = 'Unknown URL';
            if (links.length > 0) {
              const href = await links[0].getAttribute('href') || '';
              postUrl = href.startsWith('http') ? href : ('https://www.reddit.com' + href).split('?')[0];
            }

            if (postUrl !== 'Unknown URL' && !extractedUrls.has(postUrl)) {
              extractedUrls.add(postUrl);
              const textContent = await item.innerText();
              const lines = textContent.split('\n').map(l => l.trim()).filter(l => l.length > 0);

              const isAd = (await item.evaluate(el => el.tagName.toLowerCase() === 'shreddit-ad-post')) || lines.some(line => ['Promoted'].includes(line));
              if (isAd) continue;

              const author = lines.find(line => line.startsWith('u/')) ?? lines.find(line => !['Promoted'].includes(line)) ?? 'Unknown';
              const contentText = lines.filter(line => ![author, '•', 'Ad', 'Promoted'].includes(line) && !line.startsWith('Advertisement:')).slice(0, 4).join(' | ');

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
          console.log(`[RedditHateSpeechMonitor] Added 0 posts this scroll. Empty scrolls incremented to ${emptyScrolls}`);
        } else {
          emptyScrolls = 0;
          console.log(`[RedditHateSpeechMonitor] Added ${addedThisScroll} posts this scroll. Reset empty scrolls.`);
        }

        if (result.posts.length < this.postCount) {
          console.log(`[RedditHateSpeechMonitor] Scrolling down...`);
          await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
          await page.waitForTimeout(3000);
        }
      }

      result.total_posts = result.posts.length;
      console.log(`[RedditHateSpeechMonitor] Run completed successfully with ${result.total_posts} posts.`);

    } catch (error) {
      console.error('[RedditHateSpeechMonitor] Fatal error during run:', error);
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
