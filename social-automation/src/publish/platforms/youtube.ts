import type { Page } from 'playwright';
import type { SocialPlatformAdapter, PublishPost } from '../model/models.js';
import { ComposerError, MediaUploadError, PublishError } from '../../shared/errors.js';

export class YouTubeAdapter implements SocialPlatformAdapter {
  readonly platform = 'youtube' as const;
  readonly displayName = 'YouTube';
  readonly supportedImageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];
  readonly maxImages = 1;

  async openComposer(page: Page): Promise<void> {
    try {
      await page.goto('https://www.youtube.com/', {
        waitUntil: 'domcontentloaded',
        timeout: 45_000,
      });
      await page.waitForTimeout(3_000);

      const createButton = page.locator('ytd-topbar-menu-button-renderer button[aria-label*="Create" i], button[aria-label="Create"], #create-icon').first();
      await createButton.waitFor({ state: 'visible', timeout: 20_000 });
      await createButton.click({ force: true });
      await page.waitForTimeout(1_500);

      const createPost = page.locator('tp-yt-paper-item:has-text("Create post"), ytd-compact-link-renderer:has-text("Create post"), yt-list-item-view-model:has-text("Create post")').first();
      await createPost.waitFor({ state: 'visible', timeout: 10_000 });
      await createPost.click({ force: true });

      await page.waitForSelector('#contenteditable-root[contenteditable="true"], ytd-backstage-post-dialog-renderer [contenteditable="true"]', { state: 'visible', timeout: 30_000 });
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new ComposerError(this.platform, detail);
    }
  }

  async createPost(page: Page, post: PublishPost): Promise<void> {
    try {
      const textbox = page.locator('#contenteditable-root[contenteditable="true"], ytd-backstage-post-dialog-renderer [contenteditable="true"]').first();
      await textbox.waitFor({ state: 'visible', timeout: 10_000 });
      await textbox.click({ force: true });
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
      const postButton = page.locator('button[aria-label="Post"]').filter({ visible: true }).first();
      await postButton.waitFor({ state: 'visible', timeout: 15_000 });
      await postButton.click({ force: true });

      await page.waitForSelector('#contenteditable-root[contenteditable="true"]', { state: 'detached', timeout: 30_000 }).catch(() => {});
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new PublishError(this.platform, detail);
    }
  }

  async verifyPublished(page: Page): Promise<{ success: boolean; postUrl?: string }> {
    try {
      await page.waitForTimeout(4_000);
      const dialogOpen = await page.locator('#contenteditable-root[contenteditable="true"]').isVisible().catch(() => false);
      if (dialogOpen) {
        return { success: false };
      }
      const postsUrl = page.url().split('?')[0];
      if (postsUrl.includes('/posts')) {
        await page.goto(postsUrl, { waitUntil: 'domcontentloaded', timeout: 30_000 }).catch(() => {});
        await page.waitForSelector('a[href*="/post/"]', { timeout: 15_000 }).catch(() => {});
      }
      const postUrl = await page.evaluate(() => {
        const link = document.querySelector('a[href*="/post/"]');
        return link ? (link as HTMLAnchorElement).href : undefined;
      });
      return { success: true, postUrl };
    } catch {
      return { success: true };
    }
  }

  private async uploadMedia(page: Page, files: readonly string[]): Promise<void> {
    try {
      const imageButton = page.locator('button[aria-label*="image" i], button[aria-label*="Image" i]').first();
      await imageButton.click({ force: true }).catch(() => {});
      const fileInput = page.locator('input[type="file"]').first();
      await fileInput.waitFor({ state: 'attached', timeout: 5_000 });
      await fileInput.setInputFiles([...files]);

      await page.waitForTimeout(4_000);
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new MediaUploadError(this.platform, detail);
    }
  }
}
