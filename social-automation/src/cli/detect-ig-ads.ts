import { getSocialContext } from '../session/manager.js';
import { trackContext, untrackContext } from '../session/shutdown.js';
import type { BrowserContext, Page } from 'playwright';

async function extractAdDetails(context: BrowserContext, postUrl: string) {
  console.log(`\n  [AdDetails] Opening new tab for: ${postUrl}`);
  const page = await context.newPage();
  
  const details = {
    date: 'Unknown',
    likes: '0',
    comments: '0',
    views: '0',
    extractedComments: [] as string[]
  };

  try {
    await page.goto(postUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(4000); // Wait for post and comments to render

    // Extract time (usually in a <time> tag)
    const timeElements = await page.locator('time').all();
    if (timeElements.length > 0) {
      details.date = (await timeElements[0].getAttribute('datetime')) || (await timeElements[0].getAttribute('title')) || await timeElements[0].innerText();
    }

    // Extract likes, comments, views from the page text
    const textContent = await page.evaluate(() => document.body.innerText);
    
    // Look for patterns like "1,234 likes" or "1M views"
    const likesMatch = textContent.match(/([\d,KMB.]+)\s+likes?/i);
    const viewsMatch = textContent.match(/([\d,KMB.]+)\s+views?/i);
    
    if (likesMatch) details.likes = likesMatch[1];
    if (viewsMatch) details.views = viewsMatch[1];

    // Try to extract comments
    // In post detail view, comments are usually inside ul elements or just rendered as divs with username and text.
    // We'll look for elements that seem like comments (e.g. have a role="button" for reply or have standard comment styling)
    // A simpler way: grab all <span> or <div> that are part of the comments list. This is tricky due to obfuscation.
    // We'll try to find common comment structures: usually an <li> containing an <h2> (username) and <span> (comment text)
    const listItems = await page.locator('ul li, div[role="listitem"]').all();
    
    for (let i = 0; i < listItems.length && details.extractedComments.length < 10; i++) {
      try {
        const itemText = await listItems[i].innerText();
        const lines = itemText.split('\n').map(l => l.trim()).filter(l => l.length > 0);
        // Usually a comment looks like: [Username, Comment Text, Time, Reply, ...]
        if (lines.length >= 2 && lines.length < 15 && !lines.includes('Sponsored')) {
          // Filter out the main post caption which is usually very long
          if (lines[1].length > 1) {
            details.extractedComments.push(`${lines[0]}: ${lines[1]}`);
          }
        }
      } catch (e) {
        // ignore
      }
    }
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

  const context = await getSocialContext(platform);
  trackContext(context);
  
  try {
    const page = context.pages()[0] ?? await context.newPage();
    console.log(`[AdDetector] Navigating to Home page...`);
    await page.goto('https://www.instagram.com/', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(5000); 

    const maxScrolls = 120; // Scroll 100 to 150 page heights
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
          
          // On Instagram, ads can have "Sponsored" or "Ad" right under the username.
          const isAd = lines.some(line => line === 'Sponsored' || line === 'Ad');

          if (isAd) {
            // Attempt to get the post URL or external ad link
            const links = await article.locator('a').all();
            let postUrl = 'Unknown URL';
            let externalUrl = 'Unknown URL';
            
            for (const link of links) {
              const href = await link.getAttribute('href') || '';
              if (href.includes('/p/') || href.includes('/reel/')) {
                postUrl = 'https://www.instagram.com' + href.split('?')[0]; // Clean query params
              } else if (href.startsWith('http') && !href.includes('instagram.com')) {
                externalUrl = href;
              }
            }
            
            // If we can't find a standard post URL, use the external URL as the identifier
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
              
              // Extract some metadata directly from feed if visible
              const likesMatch = textContent.match(/([\d,KMB.]+)\s+likes?/i);
              const commentsMatch = textContent.match(/View all ([\d,]+)\s+comments?/i);
              
              if (likesMatch) console.log(`[Feed Metadata] Likes: ${likesMatch[1]}`);
              if (commentsMatch) console.log(`[Feed Metadata] Comments Count: ${commentsMatch[1]}`);

              // If it has an internal Instagram URL, scrape it deeply
              if (postUrl !== 'Unknown URL') {
                const details = await extractAdDetails(context, postUrl);
                console.log(`[Metadata] Date: ${details.date}`);
                console.log(`[Metadata] Likes: ${details.likes || (likesMatch ? likesMatch[1] : '0')}, Views: ${details.views}`);
                
                // Print comments found
                const validComments = details.extractedComments.filter(c => !c.includes(author)); // Filter out the caption which often gets parsed as a comment
                console.log(`[Comments Extracted]: ${validComments.length}`);
                validComments.slice(0, 5).forEach((c, idx) => {
                  console.log(`  -> Comment ${idx + 1}: ${c.substring(0, 100)}...`);
                });
              } else {
                 console.log(`[Metadata] No internal Instagram post URL found. This is a purely external ad card.`);
                 // We can try to extract visible comments in the feed
                 const visibleComments = lines.slice(-5).filter(l => !l.includes('Sponsored') && !l.includes('likes') && !l.includes('comments'));
                 console.log(`[Comments Extracted]: Feed context snippet...`);
                 console.log(`  -> ${visibleComments.join(' | ').substring(0, 150)}`);
              }
              
              console.log(`======================================\n`);
            }
          }
        } catch (err) {
          // Ignore transient errors
        }
      }

      await page.evaluate(() => window.scrollBy(0, window.innerHeight));
      await page.waitForTimeout(2500); // Instagram can be slightly slower to load
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
