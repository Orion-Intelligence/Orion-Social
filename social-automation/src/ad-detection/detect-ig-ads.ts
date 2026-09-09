import { getSocialContext } from '../session/session-manager.js';
import { trackContext, untrackContext } from '../session/shutdown.js';
import { errorReason, isSessionExpired, parseResultFileArg, writeResult } from '../shared/result-writer.js';
import type { AdDetectionResult } from './model/models.js';
import type { BrowserContext } from 'playwright';
import { MAX_SCROLLS } from './constants/constants.js';

export class InstagramAdDetector {
  private readonly platform = 'instagram';

  constructor(private readonly sessionFile?: string) {}

  async run(): Promise<AdDetectionResult> {
    console.log(`[AdDetect] Starting Instagram ad detection`);

    const result: AdDetectionResult = {
      total_detected_ads: 0,
      ads: [],
      error: false,
      error_reason: '',
      session_expired: false,
    };

    let context: BrowserContext;
    try {
      context = await getSocialContext(this.platform, 'default', this.sessionFile);
    } catch (error) {
      console.log(`[AdDetect] Could not open session: ${errorReason(error)}`);
      result.error = true;
      result.error_reason = errorReason(error);
      result.session_expired = isSessionExpired(error);
      return result;
    }

    trackContext(context);

    try {
      const page = context.pages()[0] ?? await context.newPage();
      console.log(`[AdDetect] Opening feed`);
      await page.goto('https://www.instagram.com/', { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(5000);

      const detectedAds = new Set<string>();

      console.log(`[AdDetect] Scrolling feed (${MAX_SCROLLS} scrolls)`);

      for (let i = 0; i < MAX_SCROLLS; i++) {
        console.log(`[AdDetect] Scroll ${i + 1}/${MAX_SCROLLS} - ads so far: ${result.ads.length}`);

        const articles = page.locator('article');
        const count = await articles.count();

        for (let j = 0; j < count; j++) {
          const article = articles.nth(j);

          try {
            const textContent = await article.innerText();
            const lines = textContent.split('\n').map(l => l.trim()).filter(l => l.length > 0);

            const isAd = lines.some(line => line === 'Sponsored' || line === 'Ad');

            if (isAd) {

              const links = await article.locator('a').all();
              let postUrl = 'Unknown URL';
              let externalUrl = 'Unknown URL';

              for (const link of links) {
                const href = await link.getAttribute('href') || '';
                if (href.includes('/p/') || href.includes('/reel/')) {
                  postUrl = 'https://www.instagram.com' + href.split('?')[0];
                } else if (href.startsWith('http') && !href.includes('instagram.com')) {
                  externalUrl = href;
                }
              }

              const uniqueId = postUrl !== 'Unknown URL' ? postUrl : externalUrl;

              if (uniqueId !== 'Unknown URL' && !detectedAds.has(uniqueId)) {
                detectedAds.add(uniqueId);

                const author = lines.length > 0 ? lines[0] : 'Unknown';

                const likesMatch = textContent.match(/([\d,KMB.]+)\s+likes?/i);

                let adDate = '';
                let adLikes = likesMatch ? likesMatch[1] : '0';
                let adViews = '0';

                if (postUrl !== 'Unknown URL') {
                  const details = await this.extractAdDetails(context, postUrl);
                  adDate = details.date;
                  adLikes = details.likes || (likesMatch ? likesMatch[1] : '0');
                  adViews = details.views;
                }

                result.ads.push({
                  url: uniqueId,
                  author,
                  content_text: lines.slice(2, 5).join(' | '),
                  metadata: adDate,
                  likes: adLikes,
                  shares: '',
                  views: adViews,
                  detected_at: new Date().toISOString(),
                });
                result.total_detected_ads = result.ads.length;
                console.log(`[AdDetect] Ad #${result.ads.length} found: ${author}`);

              }
            }
          } catch {
            // ignore a single article that fails to parse and continue scanning
          }
        }

        await page.evaluate(() => window.scrollBy(0, window.innerHeight));
        await page.waitForTimeout(2500);
      }

      console.log(`[AdDetect] Finished. Total ads detected: ${result.ads.length}`);

    } catch (error) {
      console.log(`[AdDetect] Failed: ${errorReason(error)}`);
      result.error = true;
      result.error_reason = errorReason(error);
      result.session_expired = isSessionExpired(error);
    } finally {
      untrackContext(context);
      await context.close();
    }

    return result;
  }

  private async extractAdDetails(context: BrowserContext, postUrl: string) {
    const page = await context.newPage();

    const details = {
      date: 'Unknown',
      likes: '0',
      views: '0'
    };

    try {
      await page.goto(postUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForTimeout(4000);

      const timeElements = await page.locator('time').all();
      if (timeElements.length > 0) {
        details.date = (await timeElements[0].getAttribute('datetime')) || (await timeElements[0].getAttribute('title')) || await timeElements[0].innerText();
      }

      const textContent = await page.evaluate(() => document.body.innerText);

      const likesMatch = textContent.match(/([\d,KMB.]+)\s+likes?/i);
      const viewsMatch = textContent.match(/([\d,KMB.]+)\s+views?/i);

      if (likesMatch) details.likes = likesMatch[1];
      if (viewsMatch) details.views = viewsMatch[1];

    } catch {
      // best-effort scrape; return whatever defaults we have on failure
    } finally {
      await page.close();
    }

    return details;
  }
}

function parseSessionFileArg(argv: string[]): string | undefined {
  const args = argv.slice(2);
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--session-file' && args[i + 1]) {
      return args[i + 1];
    }
  }
  return undefined;
}

async function main(): Promise<void> {
  const sessionFile = parseSessionFileArg(process.argv);
  const resultFile = parseResultFileArg(process.argv);

  const result = await new InstagramAdDetector(sessionFile).run();
  writeResult(resultFile, result);
}

main().catch(() => {});
