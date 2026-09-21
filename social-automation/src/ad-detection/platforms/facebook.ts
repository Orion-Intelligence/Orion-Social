import { getSocialContext } from '../../session/session-manager.js';
import { trackContext, untrackContext } from '../../session/shutdown.js';
import { errorReason, isSessionExpired } from '../../shared/result-writer.js';
import type { AdDetectionResult } from '../model/models.js';
import type { BrowserContext } from 'playwright';
import { MAX_SCROLLS, createEmptyAdDetectionResult } from '../constants/constants.js';

export class FacebookAdDetector {
  private readonly platform = 'facebook';

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
      await page.goto('https://www.facebook.com/', { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(5000);

      const detectedAds = new Set<string>();


      for (let i = 0; i < MAX_SCROLLS; i++) {

        const items = page.locator('div[aria-posinset], div[role="article"], div[data-pagelet^="FeedUnit"]');
        const count = await items.count();

        for (let j = 0; j < count; j++) {
          const item = items.nth(j);

          try {
            const textContent = await item.innerText();
            const lines = textContent.split('\n').map(l => l.trim()).filter(l => l.length > 0);

            const labels = ['Sponsored', '\u2060'];
            const noise = [...labels, 'Facebook', '·', 'Online status indicator', 'Active'];
            const isAd = lines.some(line => labels.includes(line));

            if (isAd) {
              const links = await item.locator('a[href*="/ads/"], a[href*="l.facebook.com"], a[href*="/posts/"], a[href*="/permalink/"], a[target="_blank"]').all();
              let adUrl = 'Unknown URL';
              for (const link of links) {
                const href = await link.getAttribute('href') || '';
                if (!href || href.startsWith('?') || href.startsWith('#')) continue;
                let candidate = href.startsWith('http') ? href : 'https://www.facebook.com' + href;
                if (candidate.includes('l.facebook.com')) {
                  const target = new URL(candidate).searchParams.get('u') || '';
                  if (!target.startsWith('http')) continue;
                  candidate = target;
                }
                adUrl = candidate.split('?')[0];
                break;
              }

              const headerLink = item.locator('h2 a, h3 a, h4 a, strong a').first();
              const header = await headerLink.innerText({ timeout: 1000 }).catch(() => '');
              const author = header.trim() || (lines.find(line => !noise.includes(line)) ?? 'Unknown');
              const content = lines.filter(line => !noise.includes(line) && line !== author);
              if (adUrl === 'Unknown URL') {
                const pageHref = await headerLink.getAttribute('href', { timeout: 1000 }).catch(() => '') || '';
                if (pageHref.startsWith('http')) {
                  const pageUrl = new URL(pageHref);
                  const profileId = pageUrl.searchParams.get('id');
                  adUrl = pageUrl.origin + pageUrl.pathname + (profileId ? '?id=' + profileId : '');
                }
              }

              const uniqueId = [author, ...content.slice(0, 2)].join(' | ');

              if (uniqueId && !detectedAds.has(uniqueId)) {
                detectedAds.add(uniqueId);
                const likesMatch = textContent.match(/([\d,.]+[KMB]?)\s+(likes?|upvotes?)/i);
                const viewsMatch = textContent.match(/([\d,.]+[KMB]?)\s+views?/i);

                result.ads.push({
                  url: adUrl !== 'Unknown URL' ? adUrl : page.url(),
                  author,
                  content_text: content.slice(0, 4).join(' | '),
                  metadata: '',
                  likes: likesMatch ? likesMatch[1] : '0',
                  shares: '',
                  views: viewsMatch ? viewsMatch[1] : '0',
                  detected_at: new Date().toISOString(),
                });
                result.total_detected_ads = result.ads.length;
                console.log(`[FacebookAdDetector] Ad detected: ${author} ${adUrl}`);

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
