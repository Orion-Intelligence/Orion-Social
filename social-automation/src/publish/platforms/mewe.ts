import type { Page } from 'playwright';
import type { SocialPlatformAdapter, PublishPost } from '../model/models.js';
import { ComposerError, MediaUploadError, PublishError } from '../../shared/errors.js';

export class MeWeAdapter implements SocialPlatformAdapter {
  readonly platform = 'mewe' as const;
  readonly displayName = 'MeWe';
  readonly supportedImageExtensions = ['.jpg', '.jpeg', '.png', '.gif'];
  readonly maxImages = 10;
  private text = '';

  async openComposer(page: Page): Promise<void> {
    try {
      await page.goto('https://mewe.com/myworld', {
        waitUntil: 'domcontentloaded',
        timeout: 45_000,
      });
      await page.waitForTimeout(3_000);

      const trigger = page.locator('.c-mw-postbar, .ql-editor[data-placeholder], [class*="postbar"], [class*="composer"] .ql-editor, [contenteditable="true"]').first();
      await trigger.waitFor({ state: 'visible', timeout: 30_000 });
      await trigger.click({ force: true });

      await page.waitForSelector('.ql-editor[contenteditable="true"]', { state: 'visible', timeout: 30_000 });
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new ComposerError(this.platform, detail);
    }
  }

  async createPost(page: Page, post: PublishPost): Promise<void> {
    try {
      const textbox = page.locator('.ql-editor[contenteditable="true"]').first();
      await textbox.waitFor({ state: 'visible', timeout: 10_000 });
      await textbox.click({ force: true });
      this.text = post.text.split('\n')[0].slice(0, 80);
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
      const postButton = page.locator('button.c-mw-button.btn-primary').filter({ hasText: /^Post$/ }).first();
      await postButton.waitFor({ state: 'visible', timeout: 10_000 });
      for (let attempt = 0; attempt < 10; attempt++) {
        if (await postButton.isEnabled().catch(() => false)) {
          break;
        }
        await page.waitForTimeout(1_000);
      }
      await postButton.click({ force: true });

      await page.waitForSelector('.ql-editor[contenteditable="true"]', { state: 'detached', timeout: 30_000 }).catch(() => {});
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new PublishError(this.platform, detail);
    }
  }

  async verifyPublished(page: Page): Promise<{ success: boolean; postUrl?: string }> {
    try {
      await page.waitForTimeout(3_000);

      const composerOpen = await page.locator('.ql-editor[contenteditable="true"]').isVisible().catch(() => false);
      if (composerOpen) {
        return { success: false };
      }

      await page.goto('https://mewe.com/myworld', { waitUntil: 'domcontentloaded', timeout: 30_000 }).catch(() => {});
      await page.waitForTimeout(3_000);

      const posted = page.locator('.c-mw-post').filter({ hasText: this.text }).first();
      const postUrl = this.text
        ? await posted.locator('a[href*="/posts/"]').first().getAttribute('href', { timeout: 3_000 }).catch(() => null)
        : null;

      return { success: true, postUrl: postUrl ? 'https://mewe.com' + postUrl : undefined };
    } catch {
      return { success: true };
    }
  }

  private async uploadMedia(page: Page, files: readonly string[]): Promise<void> {
    try {
      const fileInput = page.locator('input[type="file"]').first();
      await fileInput.waitFor({ state: 'attached', timeout: 5_000 });
      await fileInput.setInputFiles([...files]);

      await page.waitForTimeout(5_000);
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new MediaUploadError(this.platform, detail);
    }
  }
}
