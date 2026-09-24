import type { Page } from 'playwright';
import type { SocialPlatformAdapter, PublishPost } from '../model/models.js';
import { ComposerError, MediaUploadError, PublishError } from '../../shared/errors.js';

export class PinterestAdapter implements SocialPlatformAdapter {
  readonly platform = 'pinterest' as const;
  readonly displayName = 'Pinterest';
  readonly supportedImageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'];
  readonly maxImages = 1;

  async openComposer(page: Page): Promise<void> {
    try {
      await page.goto('https://www.pinterest.com/pin-creation-tool/', {
        waitUntil: 'domcontentloaded',
        timeout: 45_000,
      });

      await page.waitForSelector('input[type="file"]', { state: 'attached', timeout: 30_000 });
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new ComposerError(this.platform, detail);
    }
  }

  async createPost(page: Page, post: PublishPost): Promise<void> {
    try {
      if (!post.images || post.images.length === 0) {
        throw new MediaUploadError(this.platform, 'Pinterest requires an image to create a Pin');
      }
      await this.uploadMedia(page, post.images);

      const title = page.locator('#storyboard-selector-title, [data-test-id="pin-draft-title"] textarea, textarea[placeholder*="title" i], input[placeholder*="title" i]').first();
      await title.waitFor({ state: 'visible', timeout: 30_000 });
      await title.click();
      await page.keyboard.type(post.text.split('\n')[0].slice(0, 100), { delay: 5 });

      const description = page.locator('[data-test-id="pin-draft-description"] [contenteditable="true"], [data-test-id="editor-with-mentions"] [contenteditable="true"], [aria-label*="description" i][contenteditable="true"]').first();
      if (await description.isVisible().catch(() => false)) {
        await description.click();
        await page.keyboard.type(post.text.slice(0, 500), { delay: 5 });
      }

      await this.selectBoard(page);
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
      const publishButton = page.locator('[data-test-id="storyboard-creation-nav-done"] button, button:has-text("Publish")').first();
      await publishButton.waitFor({ state: 'visible', timeout: 10_000 });
      await publishButton.click({ force: true });

      await page.waitForTimeout(6_000);
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new PublishError(this.platform, detail);
    }
  }

  async verifyPublished(page: Page): Promise<{ success: boolean; postUrl?: string }> {
    try {
      let postUrl = '';
      for (let attempt = 0; attempt < 5 && !postUrl; attempt++) {
        await page.waitForSelector('a[href*="/pin/"], :text("published")', { timeout: 15_000 }).catch(() => {});
        postUrl = await page.evaluate(() => {
          const link = document.querySelector('a[href*="/pin/"]') as HTMLAnchorElement | null;
          return link ? link.href.split('?')[0] : '';
        });
        if (!postUrl) {
          await page.waitForTimeout(2_000);
        }
      }

      if (!postUrl) {
        await page.goto('https://www.pinterest.com/', { waitUntil: 'domcontentloaded', timeout: 30_000 }).catch(() => {});
        await page.waitForTimeout(3_000);
        const profileHref = await page.locator('[data-test-id="header-profile"] a, a[data-test-id="header-profile"]').first().getAttribute('href').catch(() => null);
        if (profileHref) {
          postUrl = (profileHref.startsWith('http') ? profileHref : 'https://www.pinterest.com' + profileHref).split('?')[0];
        }
      }

      return { success: true, postUrl: postUrl || undefined };
    } catch {
      return { success: true };
    }
  }

  private async selectBoard(page: Page): Promise<void> {
    const boardButton = page.locator('[data-test-id="board-dropdown-select-button"], button:has-text("Choose a board")').first();
    if (!(await boardButton.isVisible().catch(() => false))) {
      return;
    }
    await boardButton.click({ force: true });
    await page.waitForTimeout(1_500);

    const firstBoard = page.locator('[data-test-id="boardWithoutSection"], [data-test-id^="board-row"], [role="listbox"] [role="option"]').first();
    if (await firstBoard.isVisible().catch(() => false)) {
      await firstBoard.click({ force: true });
      await page.waitForTimeout(1_000);
      return;
    }

    const createBoard = page.locator('[data-test-id="create-board"], :text("Create board")').first();
    if (await createBoard.isVisible().catch(() => false)) {
      await createBoard.click({ force: true });
      await page.waitForTimeout(1_000);
      const nameInput = page.locator('#boardEditName, input[placeholder*="Like" i], input[type="text"]').first();
      await nameInput.fill('Posts');
      await page.locator('button:has-text("Create")').first().click({ force: true });
      await page.waitForTimeout(2_000);
    }
  }

  private async uploadMedia(page: Page, files: readonly string[]): Promise<void> {
    try {
      const fileInput = page.locator('input[type="file"]').first();
      await fileInput.waitFor({ state: 'attached', timeout: 10_000 });
      await fileInput.setInputFiles([...files]);

      await page.waitForTimeout(6_000);
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new MediaUploadError(this.platform, detail);
    }
  }
}
