import type { Page } from 'playwright';
import type { SocialPlatformAdapter, PublishPost } from '../model/models.js';
import { ComposerError, MediaUploadError, PublishError } from '../../shared/errors.js';

export class PatreonAdapter implements SocialPlatformAdapter {
  readonly platform = 'patreon' as const;
  readonly displayName = 'Patreon';
  readonly supportedImageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];
  readonly maxImages = 10;

  async openComposer(page: Page): Promise<void> {
    try {
      await page.goto('https://www.patreon.com/posts/new?type=text_post', {
        waitUntil: 'domcontentloaded',
        timeout: 45_000,
      });

      await page.waitForSelector(
        '[data-tag="post-title"], textarea[placeholder*="Title" i], input[placeholder*="Title" i]',
        { state: 'visible', timeout: 30_000 },
      );
      await page.waitForTimeout(2_000);

      const announcement = page.locator('[role="dialog"] button[aria-label="Close"], [role="dialog"] button:has-text("OK")').first();
      if (await announcement.isVisible().catch(() => false)) {
        await announcement.click({ timeout: 5_000 }).catch(() => {});
        await page.waitForTimeout(1_000);
      }
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new ComposerError(this.platform, detail);
    }
  }

  async createPost(page: Page, post: PublishPost): Promise<void> {
    try {
      const title = page.locator('[data-tag="post-title"], textarea[placeholder*="Title" i], input[placeholder*="Title" i]').first();
      await title.waitFor({ state: 'visible', timeout: 10_000 });
      await title.click();
      await page.keyboard.type(post.text.split('\n')[0].slice(0, 120), { delay: 5 });

      const body = page.locator('[data-tag="post-content-editor"] [contenteditable="true"], [data-tag="post-editor"] [contenteditable="true"], .ProseMirror[contenteditable="true"], [contenteditable="true"]').first();
      await body.waitFor({ state: 'visible', timeout: 10_000 });
      await body.click();
      await page.keyboard.type(post.text, { delay: 5 });

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
      const publishButton = page.locator('[data-tag="publish-button"], button:has-text("Publish now"), button:has-text("Publish")').first();
      await publishButton.waitFor({ state: 'visible', timeout: 10_000 });
      await publishButton.click({ force: true });
      await page.waitForTimeout(2_000);

      const confirm = page.locator('[role="dialog"] button:has-text("Publish now"), [role="dialog"] button:has-text("Publish")').first();
      if (await confirm.isVisible().catch(() => false)) {
        await confirm.click({ force: true });
      }

      await page.waitForURL(/\/posts\/[^/]+-\d+/, { timeout: 45_000 }).catch(() => {});
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new PublishError(this.platform, detail);
    }
  }

  async verifyPublished(page: Page): Promise<{ success: boolean; postUrl?: string }> {
    try {
      await page.waitForTimeout(3_000);
      const url = page.url().split('?')[0];
      if (/\/posts\/[^/]+-\d+/.test(url)) {
        return { success: true, postUrl: url };
      }
      const stillEditing = await page.locator('[data-tag="post-title"]').isVisible().catch(() => false);
      return { success: !stillEditing };
    } catch {
      return { success: false };
    }
  }

  private async uploadMedia(page: Page, files: readonly string[]): Promise<void> {
    try {
      const fileInput = page.locator('input[type="file"]').first();
      await fileInput.waitFor({ state: 'attached', timeout: 5_000 });
      await fileInput.setInputFiles([...files]);

      await page.waitForTimeout(6_000);
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new MediaUploadError(this.platform, detail);
    }
  }
}
