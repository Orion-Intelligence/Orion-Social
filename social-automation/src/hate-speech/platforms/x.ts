import { getSocialContext } from '../../session/session-manager.js';
import { trackContext, untrackContext } from '../../session/shutdown.js';
import { errorReason, isSessionExpired } from '../../shared/result-writer.js';
import type { HateSpeechMonitorResult } from '../model/models.js';
import type { BrowserContext } from 'playwright';
import { createEmptyHateSpeechMonitorResult } from '../constants/constants.js';
import { SocialAutomationError } from '../../shared/errors.js';

export class XHateSpeechMonitor {
  private readonly platform = 'x';

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
      console.error('[XHateSpeechMonitor] getSocialContext failed:', error);
      result.error = true;
      result.error_reason = errorReason(error);
      result.session_expired = isSessionExpired(error);
      return result;
    }

    trackContext(context);

    try {
      console.log(`[XHateSpeechMonitor] Starting run for ${this.profileUrl}`);
      const page = context.pages()[0] ?? await context.newPage();
      console.log(`[XHateSpeechMonitor] Navigating...`);
      await page.goto(this.profileUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
      console.log(`[XHateSpeechMonitor] Navigated. Waiting for timeline...`);
      try {
        await page.waitForSelector('article', { timeout: 15000 });
      } catch {
        console.log(`[XHateSpeechMonitor] Timeout waiting for articles, will proceed anyway.`);
      }
      
      if (page.url().includes('login') || (await page.locator('[data-testid="login"]').count()) > 0) {
        throw new SocialAutomationError('Session expired: Redirected to login page.', 'SESSION_EXPIRED');
      }

      console.log(`[XHateSpeechMonitor] Wait done. Start scrolling...`);

      const extractedUrls = new Set<string>();
      let emptyScrolls = 0;

      while (result.posts.length < this.postCount && emptyScrolls < 10) {
        const articles = page.locator('article');
        const count = await articles.count();
        let addedThisScroll = 0;
        console.log(`[XHateSpeechMonitor] Found ${count} articles on screen. Empty scrolls: ${emptyScrolls}, Total extracted: ${result.posts.length}`);

        for (let j = 0; j < count; j++) {
          if (result.posts.length >= this.postCount) break;

          const article = articles.nth(j);
          try {
            const links = await article.locator('a[href*="/status/"]').all();
            let tweetUrl = 'Unknown URL';
            if (links.length > 0) {
              const href = await links[0].getAttribute('href') || '';
              tweetUrl = 'https://x.com' + href;
              tweetUrl = tweetUrl.split('/analytics')[0].split('/photo')[0].split('/video')[0];
            }

            if (tweetUrl !== 'Unknown URL' && !extractedUrls.has(tweetUrl)) {
              extractedUrls.add(tweetUrl);
              const textContent = await article.innerText();
              const lines = textContent.split('\n').map(l => l.trim()).filter(l => l.length > 0);
              const author = lines.length > 0 ? lines[0] : 'Unknown';
              
              const isAd = lines.some(line => line === 'Ad' || line === 'Promoted');
              if (isAd) continue;

              let rawText = '';
              try {
                const textLocator = article.locator('[data-testid="tweetText"]').first();
                if (await textLocator.count() > 0) {
                  rawText = await textLocator.innerText({ timeout: 100 });
                }
              } catch {}
              const contentText = rawText || lines.slice(1, 4).join(' | ');

              let likes = '0', shares = '0', views = '0';
              try {
                const groupElements = article.locator('[role="group"]');
                if (await groupElements.count() > 0) {
                  const ariaLabel = await groupElements.first().getAttribute('aria-label') || '';
                  const repostsMatch = ariaLabel.match(/([\d,]+)\s+repost/i);
                  const likesMatch = ariaLabel.match(/([\d,]+)\s+like/i);
                  const viewsMatch = ariaLabel.match(/([\d,]+)\s+view/i);
                  if (repostsMatch) shares = repostsMatch[1];
                  if (likesMatch) likes = likesMatch[1];
                  if (viewsMatch) views = viewsMatch[1];
                }
              } catch {}

              result.posts.push({
                url: tweetUrl,
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
            // ignore
          }
        }

        if (addedThisScroll === 0) {
          emptyScrolls++;
          console.log(`[XHateSpeechMonitor] Added 0 posts this scroll. Empty scrolls incremented to ${emptyScrolls}`);
        } else {
          emptyScrolls = 0;
          console.log(`[XHateSpeechMonitor] Added ${addedThisScroll} posts this scroll. Reset empty scrolls.`);
        }

        if (result.posts.length < this.postCount) {
          console.log(`[XHateSpeechMonitor] Scrolling down...`);
          await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
          await page.waitForTimeout(3000);
        }
      }

      result.total_posts = result.posts.length;
      console.log(`[XHateSpeechMonitor] Run completed successfully with ${result.total_posts} posts.`);

    } catch (error) {
      console.error('[XHateSpeechMonitor] Fatal error during run:', error);
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
