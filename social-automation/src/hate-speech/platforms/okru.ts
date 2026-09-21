import { getSocialContext } from '../../session/session-manager.js';
import { trackContext, untrackContext } from '../../session/shutdown.js';
import { errorReason, isSessionExpired } from '../../shared/result-writer.js';
import type { HateSpeechMonitorResult } from '../model/models.js';
import type { BrowserContext } from 'playwright';
import { createEmptyHateSpeechMonitorResult } from '../constants/constants.js';
import { SocialAutomationError } from '../../shared/errors.js';

export class OkRuHateSpeechMonitor {
  private readonly platform = 'okru';

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
      console.error('[OkRuHateSpeechMonitor] getSocialContext failed:', error);
      result.error = true;
      result.error_reason = errorReason(error);
      result.session_expired = isSessionExpired(error);
      return result;
    }

    trackContext(context);

    try {
      console.log(`[OkRuHateSpeechMonitor] Starting run for ${this.profileUrl}`);
      const page = context.pages()[0] ?? await context.newPage();
      console.log(`[OkRuHateSpeechMonitor] Navigating...`);
      await page.goto(this.profileUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
      console.log(`[OkRuHateSpeechMonitor] Navigated. Waiting for timeline...`);
      try {
        await page.waitForSelector('.feed', { timeout: 15000 });
      } catch {
        console.log(`[OkRuHateSpeechMonitor] Timeout waiting for items, will proceed anyway.`);
      }

      if (page.url().includes('/login') || (await page.locator('#field_email, form.login-form').count()) > 0) {
        throw new SocialAutomationError('Session expired: Redirected to login page.', 'SESSION_EXPIRED');
      }

      console.log(`[OkRuHateSpeechMonitor] Wait done. Start scrolling...`);

      const extractedUrls = new Set<string>();
      let emptyScrolls = 0;

      while (result.posts.length < this.postCount && emptyScrolls < 10) {
        const items = page.locator('.feed');
        const count = await items.count();
        let addedThisScroll = 0;
        console.log(`[OkRuHateSpeechMonitor] Found ${count} items on screen. Empty scrolls: ${emptyScrolls}, Total extracted: ${result.posts.length}`);

        for (let j = 0; j < count; j++) {
          if (result.posts.length >= this.postCount) break;

          const item = items.nth(j);
          try {
            const links = await item.locator('a[href*="/topic/"], a[href^="http"]').all();
            let postUrl = 'Unknown URL';
            if (links.length > 0) {
              const href = await links[0].getAttribute('href') || '';
              postUrl = href.startsWith('http') ? href : 'https://ok.ru' + href;
              postUrl = postUrl.split('?')[0];
            }

            if (postUrl !== 'Unknown URL' && !extractedUrls.has(postUrl)) {
              extractedUrls.add(postUrl);
              const textContent = await item.innerText();
              const lines = textContent.split('\n').map(l => l.trim()).filter(l => l.length > 0);

              const isAd = (await item.locator('[name="18/ico_promote_18"], .__advert, [data-l*="advert"], [data-l*="promo"]').count()) > 0 || lines.some(line => ['Реклама', 'Advertisement', 'Sponsored', 'Promoted'].includes(line));
              if (isAd) continue;

              const author = lines.find(line => !['Реклама', 'Advertisement', 'Sponsored', 'Promoted'].includes(line)) ?? 'Unknown';
              const contentText = lines.filter(line => line !== author).slice(0, 4).join(' | ');

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
          console.log(`[OkRuHateSpeechMonitor] Added 0 posts this scroll. Empty scrolls incremented to ${emptyScrolls}`);
        } else {
          emptyScrolls = 0;
          console.log(`[OkRuHateSpeechMonitor] Added ${addedThisScroll} posts this scroll. Reset empty scrolls.`);
        }

        if (result.posts.length < this.postCount) {
          console.log(`[OkRuHateSpeechMonitor] Scrolling down...`);
          await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
          await page.waitForTimeout(3000);
        }
      }

      result.total_posts = result.posts.length;
      console.log(`[OkRuHateSpeechMonitor] Run completed successfully with ${result.total_posts} posts.`);

    } catch (error) {
      console.error('[OkRuHateSpeechMonitor] Fatal error during run:', error);
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
