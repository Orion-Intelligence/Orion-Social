import type { Page } from 'playwright';
import type { SocialPlatformAdapter, PublishPost } from '../types.js';
import { ComposerError, MediaUploadError, PublishError } from '../errors.js';

/**
 * Instagram publishing adapter.
 *
 * Instagram's web interface has limited posting capabilities compared to the
 * mobile app. The web composer supports image posts with captions.
 *
 * Workflow:
 *   1. Navigate to instagram.com
 *   2. Click the "New post" / create icon
 *   3. Upload image(s)
 *   4. Proceed through crop/filter steps
 *   5. Add caption text
 *   6. Click "Share"
 *   7. Verify publication
 */
export class InstagramAdapter implements SocialPlatformAdapter {
  readonly platform = 'instagram' as const;
  readonly displayName = 'Instagram';
  readonly supportedImageExtensions = ['.jpg', '.jpeg', '.png', '.webp'];
  readonly supportedVideoExtensions = ['.mp4', '.mov'];
  readonly maxImages = 10; // Instagram carousel supports up to 10.

  async isAuthenticated(page: Page): Promise<boolean> {
    try {
      await page.goto('https://www.instagram.com/', {
        waitUntil: 'domcontentloaded',
        timeout: 15_000,
      });

      return page.evaluate(() => {
        const url = window.location.href;
        if (url.includes('/accounts/login')) {
          return false;
        }
        const navProfile = document.querySelector('a[href*="/direct/"], svg[aria-label="Home"]');
        const createIcon = document.querySelector('svg[aria-label="New post"]');
        const navBar = document.querySelector('nav[role="navigation"]');
        return navProfile !== null || createIcon !== null || navBar !== null;
      });
    } catch {
      return false;
    }
  }

  async openComposer(page: Page): Promise<void> {
    try {
      await page.goto('https://www.instagram.com/', {
        waitUntil: 'domcontentloaded',
        timeout: 20_000,
      });

      // Click the "New post" / create button in the sidebar navigation.
      // Instagram's DOM overlays can intercept Playwright clicks, so we use evaluate to click directly.
      const clicked = await page.evaluate(() => {
        // 1. Try finding by SVG label
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
        
        // 2. Try finding by text "Create"
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

      // Briefly wait for any animations
      await page.waitForTimeout(1_000);

      // In some Instagram web layouts, clicking Create opens a dropdown instead of the modal.
      // We look for a visible "Post" option and click it.
      const clickedSubmenu = await page.evaluate(() => {
        const els = Array.from(document.querySelectorAll('span, div, a'));
        // Find visible elements with exact text "Post"
        const postEl = els.find(el => {
          if (el.textContent?.trim() !== 'Post') return false;
          const rect = el.getBoundingClientRect();
          return rect.width > 0 && rect.height > 0;
        });
        
        if (postEl && postEl instanceof HTMLElement) {
          // Find the closest clickable wrapper
          const clickable = postEl.closest('a') || postEl.closest('[role="link"]') || postEl.closest('[role="button"]') || postEl;
          if (clickable instanceof HTMLElement) {
            clickable.click();
            return true;
          }
        }
        return false;
      });

      if (clickedSubmenu) {
        // Wait briefly for the modal animation
        await page.waitForTimeout(1_000);
      }

      // Wait for the "Create new post" dialog to appear.
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
      // Instagram requires at least one image for standard posts.
      // Upload images via the file input in the dialog.
      const images = post.images ?? [];

      if (images.length > 0) {
        const fileInput = page.locator('[role="dialog"] input[type="file"]').first();
        await fileInput.waitFor({ state: 'attached', timeout: 5_000 });
        await fileInput.setInputFiles([...images]);

        // Wait for image processing.
        await page.waitForTimeout(3_000);
      }

      // Advance through crop/filter screens by clicking "Next".
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

      // Type the caption.
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

      // Wait for the sharing process to complete.
      await page.waitForTimeout(5_000);
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new PublishError(this.platform, detail);
    }
  }

  async verifyPublished(page: Page): Promise<{ success: boolean; postUrl?: string }> {
    try {
      // Instagram shows "Post shared" or the dialog closes on success.
      await page.waitForTimeout(2_000);

      const sharedText = await page.locator('text="Post shared"').isVisible().catch(() => false);
      const dialogGone = !(await page.locator('[role="dialog"]').isVisible().catch(() => true));

      const success = sharedText || dialogGone;

      // Try to get the post URL from a notification or the feed.
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
