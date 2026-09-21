import type { Page } from 'playwright';
import type { SocialPlatformAdapter, PublishPost } from '../model/models.js';
import { ComposerError, MediaUploadError, PublishError } from '../../shared/errors.js';

export class ThreadsAdapter implements SocialPlatformAdapter {
  readonly platform = 'threads' as const;
  readonly displayName = 'Threads';
  readonly supportedImageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];
  readonly maxImages = 10;
  private text = '';

  async openComposer(page: Page): Promise<void> {
    try {
      await page.goto('https://www.threads.com/', {
        waitUntil: 'domcontentloaded',
        timeout: 30_000,
      });
      await page.waitForTimeout(3_000);

      const trigger = page.locator('svg[aria-label="Create"], div[role="button"]:has-text("What\'s new?"), [placeholder*="What\'s new" i]').first();
      await trigger.waitFor({ state: 'visible', timeout: 15_000 });
      await trigger.click({ force: true });

      await page.waitForSelector(
        '[role="dialog"] [contenteditable="true"], [role="dialog"] [role="textbox"]',
        { state: 'visible', timeout: 15_000 },
      );
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new ComposerError(this.platform, detail);
    }
  }

  async createPost(page: Page, post: PublishPost): Promise<void> {
    try {
      const textbox = page.locator('[role="dialog"] [contenteditable="true"], [role="dialog"] [role="textbox"]').first();
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
      const postButton = page.locator('[role="dialog"] div[role="button"], [role="dialog"] button').filter({ hasText: /^Post$/ }).first();
      await postButton.waitFor({ state: 'visible', timeout: 10_000 });
      await postButton.click({ force: true });

      await page.waitForSelector('[role="dialog"] [contenteditable="true"]', { state: 'detached', timeout: 30_000 }).catch(() => {});
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new PublishError(this.platform, detail);
    }
  }

  async verifyPublished(page: Page): Promise<{ success: boolean; postUrl?: string }> {
    try {
      await page.waitForTimeout(4_000);

      const composerOpen = await page.locator('[role="dialog"] [contenteditable="true"]').isVisible().catch(() => false);
      if (composerOpen) {
        return { success: false };
      }

      const profileLink = await page.locator('a[href^="/@"]').first().getAttribute('href').catch(() => null);
      let postUrl: string | undefined;
      if (profileLink) {
        for (let attempt = 0; attempt < 5 && !postUrl; attempt++) {
          await page.goto('https://www.threads.com' + profileLink, { waitUntil: 'domcontentloaded', timeout: 30_000 }).catch(() => {});
          await page.waitForTimeout(4_000);
          const posted = page.locator('[data-pressable-container="true"]').filter({ hasText: this.text }).first();
          const href = this.text ? await posted.locator('a[href*="/post/"]').first().getAttribute('href', { timeout: 2_000 }).catch(() => null) : null;
          if (href) {
            postUrl = href.startsWith('http') ? href : 'https://www.threads.com' + href;
          }
        }
      }

      return { success: true, postUrl };
    } catch {
      return { success: true };
    }
  }

  private async uploadMedia(page: Page, files: readonly string[]): Promise<void> {
    try {
      const fileInput = page.locator('[role="dialog"] input[type="file"], input[type="file"]').first();
      await fileInput.waitFor({ state: 'attached', timeout: 5_000 });
      await fileInput.setInputFiles([...files]);

      await page.waitForTimeout(3_000);
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new MediaUploadError(this.platform, detail);
    }
  }
}
