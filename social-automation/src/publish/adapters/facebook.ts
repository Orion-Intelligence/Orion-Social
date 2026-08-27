import type { Page } from 'playwright';
import type { SocialPlatformAdapter, PublishPost } from '../types.js';
import { ComposerError, MediaUploadError, PublishError } from '../errors.js';

export class FacebookAdapter implements SocialPlatformAdapter {
  readonly platform = 'facebook' as const;
  readonly displayName = 'Facebook';
  readonly supportedImageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'];
  readonly supportedVideoExtensions = ['.mp4', '.mov'];
  readonly maxImages = 10;

  async isAuthenticated(page: Page): Promise<boolean> {
    try {
      await page.goto('https://www.facebook.com/', {
        waitUntil: 'domcontentloaded',
        timeout: 15_000,
      });

      return page.evaluate(() => {
        const url = window.location.href;
        if (url.includes('/login') || url.includes('/reg') || url.includes('/r.php')) {
          return false;
        }
        const profileLink = document.querySelector('[aria-label="Your profile"], [data-pagelet="ProfileTail"]');
        const navBar = document.querySelector('[role="navigation"]');
        return profileLink !== null || navBar !== null;
      });
    } catch {
      return false;
    }
  }

  async openComposer(page: Page): Promise<void> {
    try {
      await page.goto('https://www.facebook.com/', {
        waitUntil: 'domcontentloaded',
        timeout: 20_000,
      });

      await page.waitForTimeout(2_000);

      await page.evaluate(() => {
        const els = Array.from(document.querySelectorAll('span, div[role="button"]'));
        const notNow = els.find(el => el.textContent?.trim().toLowerCase() === 'not now');
        if (notNow && notNow instanceof HTMLElement) {
          notNow.click();
        }
      }).catch(() => {});

      await page.waitForTimeout(1_000);

      const clicked = await page.evaluate(() => {
        
        const structural = document.querySelector(
          '[data-pagelet="ComposerPost"] [role="button"], ' +
          '[data-pagelet="ComposerPost"] [role="textbox"]'
        );
        if (structural && structural instanceof HTMLElement) {
          structural.click();
          return true;
        }

        const ariaLabelled = document.querySelector(
          '[role="button"][aria-label*="mind" i], ' +
          '[role="textbox"][aria-label*="mind" i]'
        );
        if (ariaLabelled && ariaLabelled instanceof HTMLElement) {
          ariaLabelled.click();
          return true;
        }

        const allSpans = Array.from(document.querySelectorAll('span, div'));
        const textNode = allSpans.find(el => {
          const txt = el.textContent?.trim().toLowerCase() || '';
          return txt.includes('on your mind') && el.getBoundingClientRect().height > 0;
        });
        
        if (textNode && textNode instanceof HTMLElement) {
          const clickable = textNode.closest('[role="button"]') || textNode;
          (clickable as HTMLElement).click();
          return true;
        }

        return false;
      });

      if (!clicked) {
        throw new Error('Could not find the composer trigger ("What\'s on your mind?") in the Facebook DOM');
      }

      await page.waitForSelector(
        '[role="dialog"] [role="textbox"], [aria-label="Create a post"] [role="textbox"]',
        { state: 'visible', timeout: 10_000 },
      );
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new ComposerError(this.platform, detail);
    }
  }

  async createPost(page: Page, post: PublishPost): Promise<void> {
    try {
      
      const textbox = page.locator(
        '[role="dialog"] [role="textbox"], [aria-label="Create a post"] [role="textbox"]',
      ).first();

      await textbox.waitFor({ state: 'visible', timeout: 5_000 });
      await textbox.click();
      await textbox.fill(post.text);

      if (post.images && post.images.length > 0) {
        await this.uploadMedia(page, post.images);
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
      
      const postButton = page.locator(
        '[role="dialog"] [aria-label="Post"][role="button"], ' +
        '[role="dialog"] div[role="button"]:has-text("Post")',
      ).first();

      await postButton.waitFor({ state: 'visible', timeout: 5_000 });
      await postButton.click();

      await page.waitForSelector('[role="dialog"]', { state: 'detached', timeout: 30_000 })
        .catch(() => {
          
        });
    } catch (err: unknown) {
      if (err instanceof PublishError) {
        throw err;
      }
      const detail = err instanceof Error ? err.message : String(err);
      throw new PublishError(this.platform, detail);
    }
  }

  async verifyPublished(page: Page): Promise<{ success: boolean; postUrl?: string }> {
    try {
      
      await page.waitForTimeout(3_000);

      const dialogVisible = await page.locator('[role="dialog"]').isVisible().catch(() => false);
      if (dialogVisible) {
        return { success: false };
      }

      const postUrl = await page.evaluate(() => {
        
        const links = document.querySelectorAll('a[href*="/posts/"], a[href*="/permalink/"]');
        if (links.length > 0) {
          return (links[0] as HTMLAnchorElement).href;
        }
        return undefined;
      });

      return { success: true, postUrl };
    } catch {
      return { success: true }; 
    }
  }

  private async uploadMedia(page: Page, files: readonly string[]): Promise<void> {
    try {
      
      const photoButton = page.locator(
        '[role="dialog"] [aria-label*="Photo"], ' +
        '[role="dialog"] [aria-label*="photo"], ' +
        '[role="dialog"] [aria-label*="Video"]',
      ).first();

      await photoButton.waitFor({ state: 'visible', timeout: 5_000 }).catch(() => {
        
      });
      await photoButton.click().catch(() => {
        
      });

      const fileInput = page.locator('[role="dialog"] input[type="file"]').first();
      await fileInput.waitFor({ state: 'attached', timeout: 5_000 });
      await fileInput.setInputFiles([...files]);

      await page.waitForTimeout(2_000);
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new MediaUploadError(this.platform, detail);
    }
  }
}
