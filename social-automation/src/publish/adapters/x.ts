import type { Page } from 'playwright';
import type { SocialPlatformAdapter, PublishPost } from '../types.js';
import { ComposerError, MediaUploadError, PublishError } from '../errors.js';

export class XAdapter implements SocialPlatformAdapter {
  readonly platform = 'x' as const;
  readonly displayName = 'X (Twitter)';
  readonly supportedImageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];
  readonly supportedVideoExtensions = ['.mp4', '.mov'];
  readonly maxImages = 4;

  async isAuthenticated(page: Page): Promise<boolean> {
    try {
      await page.goto('https://x.com/home', {
        waitUntil: 'domcontentloaded',
        timeout: 15_000,
      });
      
      await page.waitForTimeout(3_000);

      return page.evaluate(() => {
        const url = window.location.href;
        if (url.includes('/i/flow/login') || url.includes('/login')) {
          return false;
        }
        const composeTweet = document.querySelector('[data-testid="SideNav_NewTweet_Button"]');
        const accountSwitcher = document.querySelector('[data-testid="SideNav_AccountSwitcher_Button"]');
        return composeTweet !== null || accountSwitcher !== null;
      });
    } catch {
      return false;
    }
  }

  async openComposer(page: Page): Promise<void> {
    try {
      
      await page.goto('https://x.com/compose/post', {
        waitUntil: 'domcontentloaded',
        timeout: 15_000,
      });

      await page.waitForSelector(
        '[data-testid="tweetTextarea_0"], [role="textbox"][data-testid="tweetTextarea_0"]',
        { state: 'visible', timeout: 10_000 },
      );
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new ComposerError(this.platform, detail);
    }
  }

  async createPost(page: Page, post: PublishPost): Promise<void> {
    try {
      const textbox = page.locator('[data-testid="tweetTextarea_0"]').first();
      await textbox.waitFor({ state: 'visible', timeout: 5_000 });
      await textbox.click();

      await page.keyboard.type(post.text, { delay: 10 });

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
      const postButton = page.locator('[data-testid="tweetButton"], [data-testid="tweetButtonInline"]').first();
      await postButton.waitFor({ state: 'visible', timeout: 5_000 });
      await postButton.click();

      await page.waitForTimeout(3_000);
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new PublishError(this.platform, detail);
    }
  }

  async verifyPublished(page: Page): Promise<{ success: boolean; postUrl?: string }> {
    try {
      
      await page.waitForTimeout(2_000);

      const url = page.url();
      
      const composerDismissed = !url.includes('/compose/');

      const postUrl = await page.evaluate(() => {
        
        const toast = document.querySelector('[data-testid="toast"] a[href*="/status/"]');
        if (toast) {
          return (toast as HTMLAnchorElement).href;
        }
        return undefined;
      });

      return { success: composerDismissed, postUrl };
    } catch {
      return { success: false };
    }
  }

  private async uploadMedia(page: Page, files: readonly string[]): Promise<void> {
    try {
      const fileInput = page.locator('input[data-testid="fileInput"], input[type="file"][accept*="image"]').first();
      await fileInput.waitFor({ state: 'attached', timeout: 5_000 });
      await fileInput.setInputFiles([...files]);

      await page.waitForTimeout(2_000);
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new MediaUploadError(this.platform, detail);
    }
  }
}
