import { getSocialContext } from '../session/manager.js';
import { trackContext, untrackContext } from '../session/shutdown.js';
import type { BrowserContext, Page } from 'playwright';

async function extractAdDetails(context: BrowserContext, postUrl: string) {
  console.log(`\n  [AdDetails] Opening new tab for: ${postUrl}`);
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
    console.error(`  [AdDetails] Failed to extract details:`, (err as Error).message);
  } finally {
    await page.close();
  }

  return details;
}

async function detectAds() {
  const platform = 'instagram';
  console.log(`[AdDetector] Starting Instagram Ad Detection...`);

  const args = process.argv.slice(2);
  let sessionFile: string | undefined;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--session-file' && args[i + 1]) {
      sessionFile = args[i + 1];
      break;
    }
  }

  const context = await getSocialContext(platform, 'default', sessionFile);
  trackContext(context);
  
  try {
    const page = context.pages()[0] ?? await context.newPage();
    console.log(`[AdDetector] Navigating to Home page...`);
    await page.goto('https://www.instagram.com/', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(5000); 

    const maxScrolls = 50;
    const detectedAds = new Set<string>();

    console.log(`[AdDetector] Starting scroll process (${maxScrolls} scrolls max)...`);

    for (let i = 0; i < maxScrolls; i++) {
      console.log(`[AdDetector] Scroll ${i + 1}/${maxScrolls}...`);

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
              console.log(`\n======================================`);
              console.log(`🚀 INSTAGRAM AD DETECTED!`);
              console.log(`Post URL: ${postUrl}`);
              if (externalUrl !== 'Unknown URL') {
                console.log(`External Ad URL: ${externalUrl}`);
              }
              
              const author = lines.length > 0 ? lines[0] : 'Unknown';
              console.log(`Author: ${author}`);
              console.log(`Content Snippet: ${lines.slice(2, 5).join(' | ')}`);
              
              const likesMatch = textContent.match(/([\d,KMB.]+)\s+likes?/i);
              
              if (likesMatch) console.log(`[Feed Metadata] Likes: ${likesMatch[1]}`);

              if (postUrl !== 'Unknown URL') {
                const details = await extractAdDetails(context, postUrl);
                console.log(`[Metadata] Date: ${details.date}`);
                console.log(`[Metadata] Likes: ${details.likes || (likesMatch ? likesMatch[1] : '0')}, Views: ${details.views}`);
              } else {
                 console.log(`[Metadata] No internal Instagram post URL found. This is a purely external ad card.`);
              }
              
              console.log(`======================================\n`);
            }
          }
        } catch (err) {
          
        }
      }

      await page.evaluate(() => window.scrollBy(0, window.innerHeight));
      await page.waitForTimeout(2500); 
    }

    console.log(`[AdDetector] Finished scanning. Total unique ads detected: ${detectedAds.size}`);
    
  } catch (error) {
    console.error(`[AdDetector] Error during execution:`, error);
  } finally {
    untrackContext(context);
    await context.close();
  }
}

detectAds().catch(console.error);
