import { getSocialContext } from '../../session/session-manager.js';
import { trackContext, untrackContext } from '../../session/shutdown.js';
import { errorReason, isSessionExpired } from '../../shared/result-writer.js';
import type { HateSpeechMonitorResult } from '../model/models.js';
import type { BrowserContext } from 'playwright';
import { createEmptyHateSpeechMonitorResult } from '../constants/constants.js';
import { SocialAutomationError } from '../../shared/errors.js';

export class QuoraHateSpeechMonitor {
  private readonly platform = 'quora';

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
      console.error('[QuoraHateSpeechMonitor] getSocialContext failed:', error);
      result.error = true;
      result.error_reason = errorReason(error);
      result.session_expired = isSessionExpired(error);
      return result;
    }

    trackContext(context);

    try {
      console.log(`[QuoraHateSpeechMonitor] Starting run for ${this.profileUrl}`);
      const page = context.pages()[0] ?? await context.newPage();
      console.log(`[QuoraHateSpeechMonitor] Navigating...`);
      await page.goto(this.profileUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
      console.log(`[QuoraHateSpeechMonitor] Navigated. Waiting for timeline...`);
      try {
        await page.waitForSelector('a[href*="/answer/"], .q-box.qu-borderAll', { timeout: 15000 });
      } catch {
        console.log(`[QuoraHateSpeechMonitor] Timeout waiting for items, will proceed anyway.`);
      }

      if (page.url().includes('/login') || (await page.locator('form[action*="/login"], input[name="email"]').count()) > 0) {
        throw new SocialAutomationError('Session expired: Redirected to login page.', 'SESSION_EXPIRED');
      }

      console.log(`[QuoraHateSpeechMonitor] Wait done. Start scrolling...`);

      const handle = this.profileUrl.replace(/\/+$/, '').split('/').filter(Boolean).pop() || 'Unknown';
      const extractedUrls = new Set<string>();
      let emptyScrolls = 0;

      while (result.posts.length < this.postCount && emptyScrolls < 10) {
        const items = page.locator('a[href*="/answer/"]');
        const count = await items.count();
        let addedThisScroll = 0;
        console.log(`[QuoraHateSpeechMonitor] Found ${count} answer links on screen. Empty scrolls: ${emptyScrolls}, Total extracted: ${result.posts.length}`);

        for (let j = 0; j < count; j++) {
          if (result.posts.length >= this.postCount) break;

          const item = items.nth(j);
          try {
            const href = await item.getAttribute('href') || '';
            if (!href.includes('/answer/')) continue;
            const postUrl = (href.startsWith('http') ? href : 'https://www.quora.com' + href).split('?')[0];
            if (extractedUrls.has(postUrl)) continue;

            const linkText = (await item.innerText().catch(() => '')).trim();
            const slug = decodeURIComponent(postUrl.split('/answer/')[0].split('/').pop() || '').replace(/-/g, ' ');
            const contentText = linkText || slug;

            extractedUrls.add(postUrl);
            result.posts.push({
              url: postUrl,
              author: handle,
              content_text: contentText,
              likes: '0',
              shares: '',
              views: '0',
              detected_at: new Date().toISOString(),
            });
            addedThisScroll++;
          } catch {}
        }

        if (addedThisScroll === 0) {
          emptyScrolls++;
          console.log(`[QuoraHateSpeechMonitor] Added 0 posts this scroll. Empty scrolls incremented to ${emptyScrolls}`);
        } else {
          emptyScrolls = 0;
          console.log(`[QuoraHateSpeechMonitor] Added ${addedThisScroll} posts this scroll. Reset empty scrolls.`);
        }

        if (result.posts.length < this.postCount) {
          console.log(`[QuoraHateSpeechMonitor] Scrolling down...`);
          await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
          await page.waitForTimeout(3000);
        }
      }

      result.total_posts = result.posts.length;
      console.log(`[QuoraHateSpeechMonitor] Run completed successfully with ${result.total_posts} posts.`);

    } catch (error) {
      console.error('[QuoraHateSpeechMonitor] Fatal error during run:', error);
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
