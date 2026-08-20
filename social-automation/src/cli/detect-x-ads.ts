import { getSocialContext } from '../session/manager.js';
import { trackContext, untrackContext } from '../session/shutdown.js';
import type { BrowserContext, Page } from 'playwright';

async function extractAdDetails(context: BrowserContext, tweetUrl: string) {
  console.log(`\n  [AdDetails] Opening new tab for: ${tweetUrl}`);
  const page = await context.newPage();
  
  const details = {
    date: 'Unknown',
    likes: '0',
    shares: '0',
    comments: '0',
    views: '0',
    extractedComments: [] as string[]
  };

  try {
    await page.goto(tweetUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(4000); // Wait for the post and replies to render

    // In a tweet detail view, the main post is usually the first article or has specific styling.
    // Time/Date is inside a <time> tag.
    const timeElements = await page.locator('time').all();
    if (timeElements.length > 0) {
      details.date = await timeElements[0].getAttribute('datetime') || await timeElements[0].innerText();
    }

    // Extract metrics. On X, metrics are usually aria-labels on the action bar buttons or specific spans.
    // Or we can look for the group role which contains the buttons.
    const groupElement = page.locator('article[data-testid="tweet"]').first().locator('[role="group"]').first();
    if (await groupElement.isVisible()) {
      const ariaLabel = await groupElement.getAttribute('aria-label') || '';
      // ariaLabel usually looks like "3 Replies, 10 Reposts, 50 Likes, 1000 Views"
      const repliesMatch = ariaLabel.match(/([\d,]+)\s+repl/i);
      const repostsMatch = ariaLabel.match(/([\d,]+)\s+repost/i);
      const likesMatch = ariaLabel.match(/([\d,]+)\s+like/i);
      const viewsMatch = ariaLabel.match(/([\d,]+)\s+view/i);

      if (repliesMatch) details.comments = repliesMatch[1];
      if (repostsMatch) details.shares = repostsMatch[1];
      if (likesMatch) details.likes = likesMatch[1];
      if (viewsMatch) details.views = viewsMatch[1];
    }

    // Scroll down to load comments
    await page.evaluate(() => window.scrollBy(0, 1000));
    await page.waitForTimeout(3000);

    // Get comment articles (skipping the first one which is the main post)
    const articles = page.locator('article[data-testid="tweet"]');
    const count = await articles.count();
    
    // Start from index 1 (0 is the main ad post)
    for (let i = 1; i < count && i <= 5; i++) { // Extract up to 5 comments
      try {
        const commentText = await articles.nth(i).innerText();
        const cleanComment = commentText.split('\n').map(l => l.trim()).filter(l => l.length > 0).join(' | ');
        if (cleanComment) {
          details.extractedComments.push(cleanComment);
        }
      } catch (e) {
        // Ignore errors reading individual comments
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
  const platform = 'x';
  console.log(`[AdDetector] Starting X (Twitter) Ad Detection...`);

  // 1. Launch browser with session
  const context = await getSocialContext(platform);
  trackContext(context);
  
  try {
    const page = context.pages()[0] ?? await context.newPage();
    console.log(`[AdDetector] Navigating to Home page...`);
    await page.goto('https://x.com/home', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(5000); // Wait for initial tweets to load

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
                // Clean the URL (drop /analytics or /photo etc)
                tweetUrl = tweetUrl.split('/analytics')[0].split('/photo')[0].split('/video')[0];
            }

            if (tweetUrl !== 'Unknown URL' && !detectedAds.has(tweetUrl)) {
              detectedAds.add(tweetUrl);
              console.log(`\n======================================`);
              console.log(`🚀 AD DETECTED!`);
              console.log(`URL: ${tweetUrl}`);
              const author = lines.length > 0 ? lines[0] : 'Unknown';
              console.log(`Author: ${author}`);
              console.log(`Content Snippet: ${lines.slice(1, 4).join(' | ')}`);
              
              // Extract metadata and comments using a new tab
              const details = await extractAdDetails(context, tweetUrl);
              console.log(`[Metadata] Date: ${details.date}`);
              console.log(`[Metadata] Likes: ${details.likes}, Shares/Reposts: ${details.shares}, Comments: ${details.comments}, Views: ${details.views}`);
              console.log(`[Comments Extracted]: ${details.extractedComments.length}`);
              details.extractedComments.forEach((c, idx) => {
                console.log(`  -> Comment ${idx + 1}: ${c.substring(0, 100)}...`);
              });
              
              console.log(`======================================\n`);
            }
          }
        } catch (err) {
          // Ignore transient errors
        }
      }

      await page.evaluate(() => window.scrollBy(0, window.innerHeight));
      await page.waitForTimeout(2000);
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
