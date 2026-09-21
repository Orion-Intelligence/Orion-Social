import { getSocialContext } from '../../session/session-manager.js';
import { trackContext, untrackContext } from '../../session/shutdown.js';
import { errorReason, isSessionExpired } from '../../shared/result-writer.js';
import type { HateSpeechMonitorResult } from '../model/models.js';
import type { BrowserContext } from 'playwright';
import { createEmptyHateSpeechMonitorResult } from '../constants/constants.js';
import { SocialAutomationError } from '../../shared/errors.js';

export class MeWeHateSpeechMonitor {
  private readonly platform = 'mewe';

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
      console.error('[MeWeHateSpeechMonitor] getSocialContext failed:', error);
      result.error = true;
      result.error_reason = errorReason(error);
      result.session_expired = isSessionExpired(error);
      return result;
    }

    trackContext(context);

    try {
      console.log(`[MeWeHateSpeechMonitor] Starting run for ${this.profileUrl}`);
      const page = context.pages()[0] ?? await context.newPage();
      console.log(`[MeWeHateSpeechMonitor] Navigating...`);
      await page.goto(this.profileUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
      console.log(`[MeWeHateSpeechMonitor] Navigated. Waiting for timeline...`);
      try {
        await page.waitForSelector('.c-mw-post', { timeout: 15000 });
      } catch {
        console.log(`[MeWeHateSpeechMonitor] Timeout waiting for posts, will proceed anyway.`);
      }

      if (page.url().includes('login') || (await page.locator('input[name="email"]').count()) > 0) {
        throw new SocialAutomationError('Session expired: Redirected to login page.', 'SESSION_EXPIRED');
      }

      console.log(`[MeWeHateSpeechMonitor] Wait done. Start scrolling...`);

      const extractedUrls = new Set<string>();
      let emptyScrolls = 0;

      while (result.posts.length < this.postCount && emptyScrolls < 10) {
        const items = page.locator('.c-mw-partner-post-view, .c-mw-post');
        const count = await items.count();
        let addedThisScroll = 0;
        console.log(`[MeWeHateSpeechMonitor] Found ${count} posts on screen. Empty scrolls: ${emptyScrolls}, Total extracted: ${result.posts.length}`);

        for (let j = 0; j < count; j++) {
          if (result.posts.length >= this.postCount) break;

          const item = items.nth(j);
          try {
            const textContent = await item.innerText();
            const lines = textContent.split('\n').map(l => l.trim()).filter(l => l.length > 0);

            const isAd = (await item.evaluate(el => el.className.includes('c-mw-partner-post-view'))) || lines.some(line => ['Promoted', 'Sponsored'].includes(line));
            if (isAd) continue;

            const links = await item.locator('a[href^="http"]').all();
            let postUrl = 'Unknown URL';
            if (links.length > 0) {
              postUrl = (await links[0].getAttribute('href') || '').split('?')[0];
            }

            if (postUrl !== 'Unknown URL' && !extractedUrls.has(postUrl)) {
              extractedUrls.add(postUrl);
              const author = lines.length > 0 ? lines[0] : 'Unknown';
              const contentText = lines.filter(line => line !== author && !line.startsWith('Watch this content')).slice(0, 4).join(' | ');

              result.posts.push({
                url: postUrl,
                author,
                content_text: contentText,
                likes: '0',
                shares: '',
                views: '0',
                detected_at: new Date().toISOString(),
              });
              addedThisScroll++;
            }
          } catch {
          }
        }

        if (addedThisScroll === 0) {
          emptyScrolls++;
          console.log(`[MeWeHateSpeechMonitor] Added 0 posts this scroll. Empty scrolls incremented to ${emptyScrolls}`);
        } else {
          emptyScrolls = 0;
          console.log(`[MeWeHateSpeechMonitor] Added ${addedThisScroll} posts this scroll. Reset empty scrolls.`);
        }

        if (result.posts.length < this.postCount) {
          console.log(`[MeWeHateSpeechMonitor] Scrolling down...`);
          await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
          await page.waitForTimeout(3000);
        }
      }

      result.total_posts = result.posts.length;
      console.log(`[MeWeHateSpeechMonitor] Run completed successfully with ${result.total_posts} posts.`);

    } catch (error) {
      console.error('[MeWeHateSpeechMonitor] Fatal error during run:', error);
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
