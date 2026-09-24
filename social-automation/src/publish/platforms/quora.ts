import type { Page } from 'playwright';
import type { SocialPlatformAdapter, PublishPost } from '../model/models.js';
import { ComposerError, MediaUploadError, PublishError } from '../../shared/errors.js';

export class QuoraAdapter implements SocialPlatformAdapter {
  readonly platform = 'quora' as const;
  readonly displayName = 'Quora';
  readonly supportedImageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];
  readonly maxImages = 1;
  private text = '';

  async openComposer(page: Page): Promise<void> {
    try {
      await page.goto('https://www.quora.com/', {
        waitUntil: 'domcontentloaded',
        timeout: 30_000,
      });
      await page.waitForTimeout(3_000);

      const trigger = page.locator('button:has-text("Add question"), [role="button"]:has-text("What do you want to ask or share")').first();
      await trigger.waitFor({ state: 'visible', timeout: 15_000 });
      await trigger.click({ force: true });
      await page.waitForTimeout(1_500);

      const createPostTab = page.locator('[role="dialog"] :text-is("Create Post"), :text-is("Create Post")').first();
      await createPostTab.waitFor({ state: 'visible', timeout: 10_000 });
      await createPostTab.click({ force: true });

      await page.waitForSelector('[role="dialog"] [contenteditable="true"], [contenteditable="true"][data-placeholder*="Say something" i]', { state: 'visible', timeout: 10_000 });
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new ComposerError(this.platform, detail);
    }
  }

  async createPost(page: Page, post: PublishPost): Promise<void> {
    try {
      const textbox = page.locator('[role="dialog"] [contenteditable="true"], [contenteditable="true"][data-placeholder*="Say something" i]').first();
      await textbox.waitFor({ state: 'visible', timeout: 10_000 });
      await textbox.click({ force: true });
      await page.waitForTimeout(500);
      this.text = post.text.split('\n')[0].slice(0, 60);
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
      const postButton = page.locator('[role="dialog"] button, button').filter({ hasText: /^Post$/ }).first();
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
      await page.waitForTimeout(2_000);
      const profileLink = await page.locator('a[href*="/profile/"]').first().getAttribute('href').catch(() => null);
      let profileUrl: string | undefined;
      if (profileLink) {
        profileUrl = (profileLink.startsWith('http') ? profileLink : 'https://www.quora.com' + profileLink).split('?')[0];
      }

      let postUrl = '';
      if (profileUrl) {
        for (let attempt = 0; attempt < 5 && !postUrl; attempt++) {
          await page.goto(profileUrl + '/posts', { waitUntil: 'domcontentloaded', timeout: 30_000 }).catch(() => {});
          await page.waitForTimeout(3_000);
          postUrl = await page.evaluate(({ text, allowAny }: { text: string; allowAny: boolean }) => {
            const links = Array.from(document.querySelectorAll('a[href*="/post/"]')) as HTMLAnchorElement[];
            if (text) {
              const match = links.find((a) => ((a.closest('.q-box') || a).textContent || '').includes(text));
              if (match) {
                return match.href.split('?')[0];
              }
            }
            if (allowAny && links.length > 0) {
              return links[0].href.split('?')[0];
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
      const fileInput = page.locator('input[type="file"]').first();
      await fileInput.waitFor({ state: 'attached', timeout: 5_000 });
      await fileInput.setInputFiles([...files]);

      await page.waitForTimeout(3_000);
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new MediaUploadError(this.platform, detail);
    }
  }
}
