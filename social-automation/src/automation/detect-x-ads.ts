import { getSocialContext } from '../session/manager.js';
import { trackContext, untrackContext } from '../session/shutdown.js';
import { errorReason, isSessionExpired, parseResultFileArg, writeResult } from '../result.js';
import type { AdDetectionResult } from '../result.js';
import type { BrowserContext } from 'playwright';

async function extractAdDetails(context: BrowserContext, tweetUrl: string) {
  const page = await context.newPage();
  
  const details = {
    date: 'Unknown',
    likes: '0',
    shares: '0',
    views: '0'
  };

  try {
    await page.goto(tweetUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(4000); 

    const timeElements = await page.locator('time').all();
    if (timeElements.length > 0) {
      details.date = await timeElements[0].getAttribute('datetime') || await timeElements[0].innerText();
    }

    const groupElement = page.locator('article[data-testid="tweet"]').first().locator('[role="group"]').first();
    if (await groupElement.isVisible()) {
      const ariaLabel = await groupElement.getAttribute('aria-label') || '';
      
      const repostsMatch = ariaLabel.match(/([\d,]+)\s+repost/i);
      const likesMatch = ariaLabel.match(/([\d,]+)\s+like/i);
      const viewsMatch = ariaLabel.match(/([\d,]+)\s+view/i);

      if (repostsMatch) details.shares = repostsMatch[1];
      if (likesMatch) details.likes = likesMatch[1];
      if (viewsMatch) details.views = viewsMatch[1];
    }

  } catch (err) {
  } finally {
    await page.close();
  }

  return details;
}

async function detectAds() {
  const platform = 'x';

  const args = process.argv.slice(2);
  let sessionFile: string | undefined;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--session-file' && args[i + 1]) {
      sessionFile = args[i + 1];
      break;
    }
  }

  const resultFile = parseResultFileArg(process.argv);
  const result: AdDetectionResult = {
    total_detected_ads: 0,
    ads: [],
    error: false,
    error_reason: '',
    session_expired: false,
  };

  let context: BrowserContext;
  try {
    context = await getSocialContext(platform, 'default', sessionFile);
  } catch (error) {
    result.error = true;
    result.error_reason = errorReason(error);
    result.session_expired = isSessionExpired(error);
    writeResult(resultFile, result);
    return;
  }

  trackContext(context);

  try {
    const page = context.pages()[0] ?? await context.newPage();
    await page.goto('https://x.com/home', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(5000); 

    const maxScrolls = 50;
    const detectedAds = new Set<string>();


    for (let i = 0; i < maxScrolls; i++) {

      const articles = page.locator('article');
      const count = await articles.count();

      for (let j = 0; j < count; j++) {
        const article = articles.nth(j);
        
        try {
          const textContent = await article.innerText();
          const lines = textContent.split('\n').map(l => l.trim()).filter(l => l.length > 0);
          
          const isAd = lines.some(line => 
            line === 'Ad' || 
            line === 'Promoted' || 
            line.toLowerCase() === 'boosted' ||
            line.toLowerCase() === 'boost'
          );

          if (isAd) {
            const links = await article.locator('a[href*="/status/"]').all();
            let tweetUrl = 'Unknown URL';
            if (links.length > 0) {
                const href = await links[0].getAttribute('href') || '';
                tweetUrl = 'https://x.com' + href;
                
                tweetUrl = tweetUrl.split('/analytics')[0].split('/photo')[0].split('/video')[0];
            }

            if (tweetUrl !== 'Unknown URL' && !detectedAds.has(tweetUrl)) {
              detectedAds.add(tweetUrl);
              const author = lines.length > 0 ? lines[0] : 'Unknown';
              
              const details = await extractAdDetails(context, tweetUrl);

              result.ads.push({
                url: tweetUrl,
                author,
                content_text: lines.slice(1, 4).join(' | '),
                metadata: details.date,
                likes: details.likes,
                shares: details.shares,
                views: details.views,
                detected_at: new Date().toISOString(),
              });
              result.total_detected_ads = result.ads.length;

            }
          }
        } catch (err) {
          
        }
      }

      await page.evaluate(() => window.scrollBy(0, window.innerHeight));
      await page.waitForTimeout(2000);
    }


  } catch (error) {
    result.error = true;
    result.error_reason = errorReason(error);
    result.session_expired = isSessionExpired(error);
  } finally {
    untrackContext(context);
    await context.close();
    writeResult(resultFile, result);
  }
}

detectAds().catch(() => {});
