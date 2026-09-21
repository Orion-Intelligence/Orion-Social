import { getSocialContext } from '../../session/session-manager.js';
import { trackContext, untrackContext } from '../../session/shutdown.js';
import { errorReason, isSessionExpired } from '../../shared/result-writer.js';
import type { AdDetectionResult } from '../model/models.js';
import type { BrowserContext } from 'playwright';
import { MAX_SCROLLS, createEmptyAdDetectionResult } from '../constants/constants.js';

export class MeWeAdDetector {
  private readonly platform = 'mewe';

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
      await page.goto('https://mewe.com/myworld', { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(5000);

      const detectedAds = new Set<string>();


      for (let i = 0; i < MAX_SCROLLS; i++) {

        const items = page.locator('.c-mw-partner-post-view, .c-mw-post');
        const count = await items.count();

        for (let j = 0; j < count; j++) {
          const item = items.nth(j);

          try {
            const textContent = await item.innerText();
            const lines = textContent.split('\n').map(l => l.trim()).filter(l => l.length > 0);

            const isAd = (await item.evaluate(el => el.className.includes('c-mw-partner-post-view'))) || lines.some(line => ['Promoted', 'Sponsored'].includes(line));

            if (isAd) {
              const links = await item.locator('a[href^="http"]').all();
              let adUrl = 'Unknown URL';
              if (links.length > 0) {
                adUrl = (await links[0].getAttribute('href') || '').split('?')[0];
              }

              const promotedIndex = lines.findIndex(line => ['Promoted', 'Sponsored'].includes(line));
              const author = promotedIndex > 0 ? lines[promotedIndex - 1] : (lines.find(line => !['Promoted', 'Sponsored'].includes(line)) ?? 'Unknown');
              const uniqueId = `${author} | ${lines.slice(0, 3).join(' | ')}`;

              if (!detectedAds.has(uniqueId)) {
                detectedAds.add(uniqueId);

                result.ads.push({
                  url: adUrl !== 'Unknown URL' ? adUrl : page.url(),
                  author,
                  content_text: lines.filter(line => ![author, 'Promoted', 'Sponsored'].includes(line) && !line.startsWith('Watch this content')).slice(0, 4).join(' | '),
                  metadata: '',
                  likes: '0',
                  shares: '',
                  views: '0',
                  detected_at: new Date().toISOString(),
                });
                result.total_detected_ads = result.ads.length;
                console.log(`[MeWeAdDetector] Ad detected: ${author} ${adUrl}`);

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
