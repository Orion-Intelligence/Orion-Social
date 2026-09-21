import { getSocialContext } from '../../session/session-manager.js';
import { trackContext, untrackContext } from '../../session/shutdown.js';
import { errorReason, isSessionExpired } from '../../shared/result-writer.js';
import type { AdDetectionResult } from '../model/models.js';
import type { BrowserContext } from 'playwright';
import { MAX_SCROLLS, createEmptyAdDetectionResult } from '../constants/constants.js';

export class ThreadsAdDetector {
  private readonly platform = 'threads';

  constructor(private readonly sessionFile?: string) {}

  async run(): Promise<AdDetectionResult> {

    const result = createEmptyAdDetectionResult();

    let context: BrowserContext;
    try {
      context = await getSocialContext(this.platform, 'default', this.sessionFile);
    } catch (error) {
      result.error = true;
      result.error_reason = errorReason(error);
      result.session_expired = isSessionExpired(error);
      return result;
    }

    trackContext(context);

    try {
      const page = context.pages()[0] ?? await context.newPage();
      await page.goto('https://www.threads.com/', { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(5000);

      const detectedAds = new Set<string>();
      const SCAN_WINDOW = 40;
      const deadline = Date.now() + 720000;


      for (let i = 0; i < MAX_SCROLLS; i++) {

        if (Date.now() > deadline) {
          break;
        }

        const items = page.locator('[data-pressable-container="true"]');
        const count = await items.count();
        const start = Math.max(0, count - SCAN_WINDOW);

        for (let j = start; j < count; j++) {
          const item = items.nth(j);

          try {
            const textContent = await item.innerText({ timeout: 1000 });
            const lines = textContent.split('\n').map(l => l.trim()).filter(l => l.length > 0);

            const isAd = lines.some(line => ['Sponsored'].includes(line));

            if (isAd) {
              const links = await item.locator('a[href*="/post/"]').all();
              let adUrl = 'Unknown URL';
              if (links.length > 0) {
                const href = await links[0].getAttribute('href') || '';
                adUrl = href.startsWith('http') ? href : 'https://www.threads.com' + href;
                adUrl = adUrl.split('?')[0];
              }

              const uniqueId = adUrl !== 'Unknown URL' ? adUrl : lines.slice(0, 3).join(' | ');

              if (uniqueId && !detectedAds.has(uniqueId)) {
                detectedAds.add(uniqueId);
                const author = lines.find(line => !['Sponsored'].includes(line)) ?? 'Unknown';
                const likesMatch = textContent.match(/([\d,.]+[KMB]?)\s+(likes?|upvotes?)/i);
                const viewsMatch = textContent.match(/([\d,.]+[KMB]?)\s+views?/i);

                result.ads.push({
                  url: adUrl !== 'Unknown URL' ? adUrl : page.url(),
                  author,
                  content_text: lines.filter(line => line !== author).slice(0, 4).join(' | '),
                  metadata: '',
                  likes: likesMatch ? likesMatch[1] : '0',
                  shares: '',
                  views: viewsMatch ? viewsMatch[1] : '0',
                  detected_at: new Date().toISOString(),
                });
                result.total_detected_ads = result.ads.length;
                console.log(`[ThreadsAdDetector] Ad detected: ${author} ${adUrl}`);

              }
            }
          } catch {
            // ignore a single item that fails to parse and continue scanning
          }
        }

        await page.evaluate(() => window.scrollBy(0, window.innerHeight));
        await page.waitForTimeout(2500);
      }


    } catch (error) {
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
