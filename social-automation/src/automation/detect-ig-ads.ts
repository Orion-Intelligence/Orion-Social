import { getSocialContext } from '../session/manager.js';
import { trackContext, untrackContext } from '../session/shutdown.js';
import { errorReason, isSessionExpired, parseResultFileArg, writeResult } from '../result.js';
import type { AdDetectionResult } from '../result.js';
import type { BrowserContext } from 'playwright';

async function extractAdDetails(context: BrowserContext, postUrl: string) {
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

  } catch (err) {
  } finally {
    await page.close();
  }

  return details;
}

async function detectAds() {
  const platform = 'instagram';

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
    await page.goto('https://www.instagram.com/', { waitUntil: 'domcontentloaded' });
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
              if (externalUrl !== 'Unknown URL') {
              }
              
              const author = lines.length > 0 ? lines[0] : 'Unknown';
              
              const likesMatch = textContent.match(/([\d,KMB.]+)\s+likes?/i);
              

              let adDate = '';
              let adLikes = likesMatch ? likesMatch[1] : '0';
              let adViews = '0';

              if (postUrl !== 'Unknown URL') {
                const details = await extractAdDetails(context, postUrl);
                adDate = details.date;
                adLikes = details.likes || (likesMatch ? likesMatch[1] : '0');
                adViews = details.views;
              } else {
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

            }
          }
        } catch (err) {
          
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
    writeResult(resultFile, result);
  }
}

detectAds().catch(() => {});
