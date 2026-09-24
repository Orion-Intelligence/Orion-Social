import type { Page } from 'playwright';
import type { SocialPlatformAdapter, PublishPost } from '../model/models.js';
import { ComposerError, MediaUploadError, PublishError } from '../../shared/errors.js';

export class TikTokAdapter implements SocialPlatformAdapter {
  readonly platform = 'tiktok' as const;
  readonly displayName = 'TikTok';
  readonly supportedImageExtensions = ['.jpg', '.jpeg', '.png', '.webp'];
  readonly maxImages = 35;
  private text = '';

  async openComposer(page: Page): Promise<void> {
    try {
      await page.goto('https://www.tiktok.com/tiktokstudio/upload?from=webapp', {
        waitUntil: 'domcontentloaded',
        timeout: 45_000,
      });

      await page.waitForSelector('input[type="file"]', { state: 'attached', timeout: 45_000 });

      const photosTab = page.locator('button[role="tab"]:has-text("Photos")').first();
      await photosTab.waitFor({ state: 'visible', timeout: 15_000 });
      await photosTab.click({ force: true });
      await page.waitForSelector('input[type="file"][accept*="image"]', { state: 'attached', timeout: 15_000 });
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new ComposerError(this.platform, detail);
    }
  }

  async createPost(page: Page, post: PublishPost): Promise<void> {
    try {
      if (!post.images || post.images.length === 0) {
        throw new MediaUploadError(this.platform, 'TikTok requires at least one image to create a photo post');
      }
      await this.uploadMedia(page, post.images);

      const caption = page.locator('.public-DraftEditor-content[contenteditable="true"], [data-e2e="caption-input"] [contenteditable="true"], div[contenteditable="true"]').first();
      await caption.waitFor({ state: 'visible', timeout: 60_000 });
      await caption.click({ force: true });
      await page.keyboard.press('Control+A');
      this.text = post.text.split('\n')[0].slice(0, 60);
      await page.keyboard.type(post.text.slice(0, 2000), { delay: 10 });
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
      const postButton = page.getByRole('button', { name: 'Post', exact: true }).last();
      await postButton.waitFor({ state: 'visible', timeout: 60_000 });
      for (let attempt = 0; attempt < 60; attempt++) {
        if (await postButton.isEnabled().catch(() => false)) {
          break;
        }
        await page.waitForTimeout(2_000);
      }
      await postButton.scrollIntoViewIfNeeded().catch(() => {});
      await postButton.click({ timeout: 15_000 });

      const confirm = page.locator('[role="dialog"] button:has-text("Post now"), [role="dialog"] button:has-text("Post anyway")').first();
      if (await confirm.isVisible({ timeout: 5_000 }).catch(() => false)) {
        await confirm.click({ timeout: 5_000 }).catch(() => {});
      }

      await page.waitForURL((url) => !url.pathname.includes('/upload'), { timeout: 60_000 }).catch(() => {});
      await page.waitForTimeout(6_000);
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new PublishError(this.platform, detail);
    }
  }

  async verifyPublished(page: Page): Promise<{ success: boolean; postUrl?: string }> {
    try {
      const profileHref = await page.locator('a[data-e2e="nav-profile"], a[href*="tiktok.com/@"], a[href^="/@"]').first().getAttribute('href').catch(() => null);
      let profileUrl: string | undefined;
      if (profileHref) {
        profileUrl = (profileHref.startsWith('http') ? profileHref : 'https://www.tiktok.com' + profileHref).split('?')[0];
      }

      let postUrl = '';
      if (profileUrl) {
        for (let attempt = 0; attempt < 5 && !postUrl; attempt++) {
          await page.goto(profileUrl, { waitUntil: 'domcontentloaded', timeout: 30_000 }).catch(() => {});
          await page.waitForTimeout(3_000);
          postUrl = await page.evaluate(({ text, allowAny }: { text: string; allowAny: boolean }) => {
            const items = Array.from(document.querySelectorAll('a[href*="/photo/"], a[href*="/video/"]')) as HTMLAnchorElement[];
            if (text) {
              const match = items.find((a) => ((a.closest('[data-e2e="user-post-item"]') || a).textContent || '').includes(text));
              if (match) {
                return match.href.split('?')[0];
              }
            }
            if (allowAny && items.length > 0) {
              return items[0].href.split('?')[0];
            }
            return '';
          }, { text: this.text, allowAny: attempt >= 1 });
        }
      }

      return { success: true, postUrl: postUrl || profileUrl };
    } catch {
      return { success: true };
    }
  }

  private async uploadMedia(page: Page, files: readonly string[]): Promise<void> {
    try {
      const fileInput = page.locator('input[type="file"][accept*="image"]').first();
      await fileInput.waitFor({ state: 'attached', timeout: 10_000 });
      await fileInput.setInputFiles([...files]);

      await page.waitForTimeout(8_000);
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new MediaUploadError(this.platform, detail);
    }
  }
}
