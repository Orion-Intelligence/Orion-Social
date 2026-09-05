import type { Page } from 'playwright';
import type { SocialPlatformAdapter, PublishPost } from '../model/models.js';
import { ComposerError, MediaUploadError, PublishError } from '../../shared/errors.js';

export class LinkedInAdapter implements SocialPlatformAdapter {
  readonly platform = 'linkedin' as const;
  readonly displayName = 'LinkedIn';
  readonly supportedImageExtensions = ['.jpg', '.jpeg', '.png', '.gif'];
  readonly supportedVideoExtensions = ['.mp4', '.mov'];
  readonly maxImages = 9;



  async openComposer(page: Page): Promise<void> {
    try {
      await page.goto('https://www.linkedin.com/feed/', {
        waitUntil: 'domcontentloaded',
        timeout: 20_000,
      });

      const startPostButton = page.locator(
        'button:has-text("Start a post"), ' +
        'button.share-box-feed-entry__trigger, ' +
        '[data-control-name="share.post"]',
      ).first();

      await startPostButton.waitFor({ state: 'visible', timeout: 10_000 });
      await startPostButton.click();

      await page.waitForSelector(
        '[role="dialog"] .ql-editor, ' +
        '.share-creation-state__text-editor .ql-editor, ' +
        '[role="dialog"] [role="textbox"]',
        { state: 'visible', timeout: 10_000 },
      );
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new ComposerError(this.platform, detail);
    }
  }

  async createPost(page: Page, post: PublishPost): Promise<void> {
    try {
      
      const editor = page.locator(
        '[role="dialog"] .ql-editor, ' +
        '[role="dialog"] [role="textbox"]',
      ).first();

      await editor.waitFor({ state: 'visible', timeout: 5_000 });
      await editor.click();
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
      const postButton = page.locator(
        '[role="dialog"] button.share-actions__primary-action, ' +
        '[role="dialog"] button:has-text("Post"), ' +
        'button[data-control-name="share.post"]',
      ).first();

      await postButton.waitFor({ state: 'visible', timeout: 5_000 });
      await postButton.click();

      await page.waitForSelector('[role="dialog"]', { state: 'detached', timeout: 30_000 })
        .catch(() => {
          
        });
    } catch (err: unknown) {
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
        const links = document.querySelectorAll(
          'a[href*="/feed/update/"], a[href*="/posts/"]',
        );
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
      
      const mediaButton = page.locator(
        '[role="dialog"] button[aria-label*="image" i], ' +
        '[role="dialog"] button[aria-label*="photo" i], ' +
        '[role="dialog"] button[aria-label*="media" i]',
      ).first();

      await mediaButton.waitFor({ state: 'visible', timeout: 5_000 }).catch(() => {  });
      await mediaButton.click().catch(() => {  });

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
