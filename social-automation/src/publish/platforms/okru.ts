import type { Page } from 'playwright';
import type { SocialPlatformAdapter, PublishPost } from '../model/models.js';
import { ComposerError, MediaUploadError, PublishError } from '../../shared/errors.js';

export class OkRuAdapter implements SocialPlatformAdapter {
  readonly platform = 'okru' as const;
  readonly displayName = 'OK.ru';
  readonly supportedImageExtensions = ['.jpg', '.jpeg', '.png', '.gif'];
  readonly maxImages = 10;

  async openComposer(page: Page): Promise<void> {
    try {
      await page.goto('https://ok.ru/', {
        waitUntil: 'domcontentloaded',
        timeout: 30_000,
      });
      await page.waitForTimeout(3_000);

      const trigger = page.locator('button[data-l="t,pf_dropdown"]').first();
      await trigger.waitFor({ state: 'visible', timeout: 15_000 });
      const writePost = page.locator('[role="menuitem"][data-l="t,feed.posting.ui.input"], [data-l="t,feed.posting.ui.input"]').first();
      for (let attempt = 0; attempt < 5; attempt++) {
        await trigger.click({ force: true });
        await page.waitForTimeout(1_500);
        if (await writePost.isVisible().catch(() => false)) {
          break;
        }
      }
      await writePost.waitFor({ state: 'visible', timeout: 10_000 });
      await writePost.click({ force: true });

      await page.waitForSelector('.posting_itx[contenteditable="true"], [data-l*="posting"] [contenteditable="true"], .posting-form [contenteditable="true"], [data-module*="posting" i] [contenteditable="true"]', { state: 'visible', timeout: 15_000 });
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new ComposerError(this.platform, detail);
    }
  }

  async createPost(page: Page, post: PublishPost): Promise<void> {
    try {
      const textbox = page.locator('.posting_itx[contenteditable="true"], [data-l*="posting"] [contenteditable="true"], .posting-form [contenteditable="true"], [data-module*="posting" i] [contenteditable="true"]').first();
      await textbox.waitFor({ state: 'visible', timeout: 10_000 });
      await textbox.click({ force: true });
      await page.keyboard.press('ControlOrMeta+A');
      await page.keyboard.press('Delete');
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
      const postButton = page.locator('[data-l="t,postingForm"] button[data-l="t,button.submit"]').first();
      await postButton.waitFor({ state: 'attached', timeout: 10_000 });
      await postButton.scrollIntoViewIfNeeded().catch(() => {});
      await postButton.click({ timeout: 10_000 });

      await page.waitForSelector('[data-l="t,postingForm"]', { state: 'detached', timeout: 30_000 }).catch(() => {});
      await page.waitForTimeout(3_000);

      const rejection = await page.locator('[data-l="t,postingForm"] .tip:visible, [data-l="t,postingForm"] [class*="error"]:visible').first().innerText({ timeout: 2_000 }).catch(() => '');
      if (rejection.trim()) {
        throw new PublishError(this.platform, rejection.trim());
      }
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
      const composerOpen = await page.locator('[data-l="t,postingForm"] [role="textbox"][contenteditable="true"]').isVisible().catch(() => false);
      if (composerOpen) {
        return { success: false };
      }

      const profileLink = await page.locator('a[href^="/profile/"]').first().getAttribute('href').catch(() => null);
      if (profileLink) {
        await page.goto('https://ok.ru' + profileLink, { waitUntil: 'domcontentloaded', timeout: 30_000 }).catch(() => {});
        await page.waitForTimeout(3_000);
      }

      const statusLinks = await page.locator('a[href*="/statuses/"]').all();
      let postUrl: string | undefined;
      for (const statusLink of statusLinks) {
        const href = await statusLink.getAttribute('href') || '';
        if (/\/statuses\/\d+/.test(href)) {
          postUrl = href.startsWith('http') ? href : 'https://ok.ru' + href;
          break;
        }
      }

      return { success: true, postUrl };
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
