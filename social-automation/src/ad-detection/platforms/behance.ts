import { getSocialContext } from '../../session/session-manager.js';
import { trackContext, untrackContext } from '../../session/shutdown.js';
import { errorReason, isSessionExpired } from '../../shared/result-writer.js';
import type { AdDetectionResult } from '../model/models.js';
import type { BrowserContext } from 'playwright';
import { MAX_SCROLLS, createEmptyAdDetectionResult } from '../constants/constants.js';

export class BehanceAdDetector {
  private readonly platform = 'behance';

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
      await page.goto('https://www.behance.net/', { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(5000);

      const detectedAds = new Set<string>();


      for (let i = 0; i < MAX_SCROLLS; i++) {

        const items = page.locator('[class*="ProjectCoverNeue"]');
        const count = await items.count();

        for (let j = 0; j < count; j++) {
          const item = items.nth(j);

          try {
            const textContent = await item.innerText();
            const lines = textContent.split('\n').map(l => l.trim()).filter(l => l.length > 0);

            const isAd = lines.some(line => ['Sponsored', 'Promoted', 'Ad'].includes(line));

            if (isAd) {
              const links = await item.locator('a[href*="/gallery/"]').all();
              let adUrl = 'Unknown URL';
              if (links.length > 0) {
                const href = await links[0].getAttribute('href') || '';
                adUrl = href.startsWith('http') ? href : 'https://www.behance.net' + href;
                adUrl = adUrl.split('?')[0];
              }

              const uniqueId = adUrl !== 'Unknown URL' ? adUrl : lines.slice(0, 3).join(' | ');

              if (uniqueId && !detectedAds.has(uniqueId)) {
                detectedAds.add(uniqueId);
                const author = lines.find(line => !['Sponsored', 'Promoted', 'Ad'].includes(line)) ?? 'Unknown';
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
                console.log(`[BehanceAdDetector] Ad detected: ${author} ${adUrl}`);

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
