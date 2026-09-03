import type { Page } from 'playwright';
import type { SocialPlatformAdapter, PublishPost } from '../../types.js';
import { ComposerError, MediaUploadError, PublishError } from '../../errors.js';

export class InstagramAdapter implements SocialPlatformAdapter {
  readonly platform = 'instagram' as const;
  readonly displayName = 'Instagram';
  readonly supportedImageExtensions = ['.jpg', '.jpeg', '.png', '.webp'];
  readonly supportedVideoExtensions = ['.mp4', '.mov'];
  readonly maxImages = 10; 


  async openComposer(page: Page): Promise<void> {
    try {
      await page.goto('https://www.instagram.com/', {
        waitUntil: 'domcontentloaded',
        timeout: 20_000,
      });

      const clicked = await page.evaluate(() => {
        
        const svg = document.querySelector('svg[aria-label="New post"], svg[aria-label="New Post"]');
        if (svg) {
          const clickable = svg.closest('a') || svg.closest('[role="link"]') || svg.closest('[role="button"]') || svg;
          if (clickable instanceof HTMLElement) {
            clickable.click();
            return true;
          } else if (clickable instanceof SVGElement) {
            clickable.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
            return true;
          }
        }
        
        const spans = Array.from(document.querySelectorAll('span, div'));
        const createEl = spans.find(el => el.textContent?.trim() === 'Create');
        if (createEl && createEl instanceof HTMLElement) {
          createEl.click();
          return true;
        }

        return false;
      });

      if (!clicked) {
        throw new Error('Could not find the Create button in the Instagram DOM');
      }

      await page.waitForTimeout(1_000);

      const clickedSubmenu = await page.evaluate(() => {
        const els = Array.from(document.querySelectorAll('span, div, a'));
        
        const postEl = els.find(el => {
          if (el.textContent?.trim() !== 'Post') return false;
          const rect = el.getBoundingClientRect();
          return rect.width > 0 && rect.height > 0;
        });
        
        if (postEl && postEl instanceof HTMLElement) {
          
          const clickable = postEl.closest('a') || postEl.closest('[role="link"]') || postEl.closest('[role="button"]') || postEl;
          if (clickable instanceof HTMLElement) {
            clickable.click();
            return true;
          }
        }
        return false;
      });

      if (clickedSubmenu) {
        
        await page.waitForTimeout(1_000);
      }

      await page.waitForSelector(
        '[role="dialog"], div[aria-label="Create new post"], div[aria-label="Create new post"] >> visible=true',
        { state: 'visible', timeout: 10_000 },
      );
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new ComposerError(this.platform, detail);
    }
  }

  async createPost(page: Page, post: PublishPost): Promise<void> {
    try {
      
      const images = post.images ?? [];

      if (images.length > 0) {
        const fileInput = page.locator('[role="dialog"] input[type="file"]').first();
        await fileInput.waitFor({ state: 'attached', timeout: 5_000 });
        await fileInput.setInputFiles([...images]);

        await page.waitForTimeout(3_000);
      }

      for (let step = 0; step < 2; step++) {
        const nextButton = page.locator(
          '[role="dialog"] button:has-text("Next"), ' +
          '[role="dialog"] [role="button"]:has-text("Next")',
        ).first();

        const nextVisible = await nextButton.isVisible().catch(() => false);
        if (nextVisible) {
          await nextButton.click();
          await page.waitForTimeout(1_000);
        }
      }

      const captionBox = page.locator(
        '[role="dialog"] [aria-label*="caption" i], ' +
        '[role="dialog"] [aria-label*="Write a caption" i], ' +
        '[role="dialog"] textarea',
      ).first();

      const captionVisible = await captionBox.isVisible().catch(() => false);
      if (captionVisible) {
        await captionBox.click();
        await page.keyboard.type(post.text, { delay: 10 });
      }
    } catch (err: unknown) {
      if (err instanceof ComposerError || err instanceof MediaUploadError) {
        throw err;
      }
      const detail = err instanceof Error ? err.message : String(err);
      throw new ComposerError(this.platform, `Failed to create post: ${detail}`);
    }
  }

  async publishPost(page: Page): Promise<void> {
    try {
      const shareButton = page.locator(
        '[role="dialog"] button:has-text("Share"), ' +
        '[role="dialog"] [role="button"]:has-text("Share")',
      ).first();

      await shareButton.waitFor({ state: 'visible', timeout: 5_000 });
      await shareButton.click();

      await page.waitForTimeout(5_000);
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new PublishError(this.platform, detail);
    }
  }

  async verifyPublished(page: Page): Promise<{ success: boolean; postUrl?: string }> {
    try {
      
      await page.waitForTimeout(2_000);

      const sharedText = await page.locator('text="Post shared"').isVisible().catch(() => false);
      const dialogGone = !(await page.locator('[role="dialog"]').isVisible().catch(() => true));

      const success = sharedText || dialogGone;

      const postUrl = await page.evaluate(() => {
        const links = document.querySelectorAll('a[href*="/p/"]');
        if (links.length > 0) {
          return (links[0] as HTMLAnchorElement).href;
        }
        return undefined;
      });

      return { success, postUrl };
    } catch {
      return { success: false };
    }
  }
}
