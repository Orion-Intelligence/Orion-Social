import type { Page } from 'playwright';
import type { SocialPlatformAdapter, PublishPost } from '../model/models.js';
import { ComposerError, MediaUploadError, PublishError } from '../../shared/errors.js';

export class BehanceAdapter implements SocialPlatformAdapter {
  readonly platform = 'behance' as const;
  readonly displayName = 'Behance';
  readonly supportedImageExtensions = ['.jpg', '.jpeg', '.png', '.gif'];
  readonly maxImages = 10;

  private image = '';
  private title = '';

  async openComposer(page: Page): Promise<void> {
    try {
      await page.goto('https://www.behance.net/portfolio/editor', {
        waitUntil: 'domcontentloaded',
        timeout: 45_000,
      });

      await page.waitForSelector('[aria-label="Add an Image"], button.js-add-file', { state: 'visible', timeout: 30_000 });
      await page.waitForTimeout(5_000);
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new ComposerError(this.platform, detail);
    }
  }

  async createPost(page: Page, post: PublishPost): Promise<void> {
    try {
      if (!post.images || post.images.length === 0) {
        throw new MediaUploadError(this.platform, 'Behance requires at least one image to create a project');
      }
      this.image = post.images[0];
      this.title = post.text.split('\n')[0].slice(0, 55);
      await this.uploadMedia(page, post.images);
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
      const openDialog = page.locator('button').filter({ hasText: /^Publish$/ }).first();
      await openDialog.waitFor({ state: 'visible', timeout: 15_000 });
      await openDialog.click({ force: true });

      const cover = page.locator('input[type="file"], input[aria-label="Upload Image"], input[name="qqfile"]').first();
      const coverPresent = await cover.waitFor({ state: 'attached', timeout: 8_000 }).then(() => true).catch(() => false);
      if (coverPresent) {
        await cover.setInputFiles(this.image);
        await page.waitForTimeout(6_000);
      }

      const title = page.locator('input[placeholder="Give your project a title"]').first();
      await title.waitFor({ state: 'visible', timeout: 15_000 });
      await title.fill(this.title);

      const categoryBox = page.getByText('How Would You Categorize This Project?', { exact: false }).first();
      if (await categoryBox.isVisible().catch(() => false)) {
        await categoryBox.click({ force: true });
        await page.waitForTimeout(1_500);
        const category = page.getByText('Graphic Design', { exact: true }).first();
        if (await category.isVisible().catch(() => false)) {
          await category.click({ force: true });
          await page.waitForTimeout(1_000);
        }
      }

      const publishButton = page.locator('button').filter({ hasText: /^Publish$/ }).last();
      await publishButton.waitFor({ state: 'visible', timeout: 10_000 });
      await publishButton.evaluate((el) => (el as HTMLElement).click());

      await page.waitForURL(/\/gallery\//, { timeout: 60_000 }).catch(() => {});
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new PublishError(this.platform, detail);
    }
  }

  async verifyPublished(page: Page): Promise<{ success: boolean; postUrl?: string }> {
    try {
      await page.waitForURL(/\/gallery\//, { timeout: 20_000 }).catch(() => undefined);
      const url = page.url().split('?')[0];
      if (url.includes('/gallery/')) {
        return { success: true, postUrl: url };
      }
      return { success: false };
    } catch {
      return { success: false };
    }
  }

  private async uploadMedia(page: Page, files: readonly string[]): Promise<void> {
    try {
      const [chooser] = await Promise.all([
        page.waitForEvent('filechooser', { timeout: 15_000 }),
        page.locator('[aria-label="Add an Image"], button.js-add-file').first().click({ force: true }),
      ]);
      await chooser.setFiles([...files]);

      await page.waitForTimeout(8_000);
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new MediaUploadError(this.platform, detail);
    }
  }
}
