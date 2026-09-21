import type { Page } from 'playwright';
import type { SocialPlatformAdapter, PublishPost } from '../model/models.js';
import { ComposerError, MediaUploadError, PublishError } from '../../shared/errors.js';

export class HashnodeAdapter implements SocialPlatformAdapter {
  readonly platform = 'hashnode' as const;
  readonly displayName = 'Hashnode';
  readonly supportedImageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];
  readonly maxImages = 1;

  async openComposer(page: Page): Promise<void> {
    try {
      await page.goto('https://hashnode.com/', {
        waitUntil: 'domcontentloaded',
        timeout: 45_000,
      });
      await page.waitForTimeout(3_000);

      const createPublication = page.locator('button:has-text("Create your first publication"), a:has-text("Create your first publication")').first();
      if (await createPublication.isVisible().catch(() => false)) {
        await createPublication.click({ force: true });
        await page.waitForTimeout(2_000);
        const nameInput = page.locator('#blog-name, input[placeholder*="Publication" i]').first();
        await nameInput.waitFor({ state: 'visible', timeout: 15_000 });
        await nameInput.click();
        await page.keyboard.type('Orion Notes', { delay: 20 });
        const subdomainInput = page.locator('#blog-subdomain, input[placeholder="my-blog"]').first();
        if (await subdomainInput.isVisible().catch(() => false)) {
          await subdomainInput.click();
          await page.keyboard.press('Control+A');
          await page.keyboard.type(`orion-notes-${Date.now().toString(36)}`, { delay: 20 });
        }
        const createButton = page.locator('button:has-text("Create Publication")').first();
        await page.waitForFunction(() => {
          const button = Array.from(document.querySelectorAll('button')).find(el => el.textContent?.trim() === 'Create Publication');
          return button !== undefined && !button.disabled;
        }, undefined, { timeout: 15_000 }).catch(() => {});
        await createButton.click({ force: true });
        await page.waitForSelector('button:has-text("Create Publication")', { state: 'detached', timeout: 30_000 }).catch(() => {});
        await page.waitForTimeout(3_000);
        await page.goto('https://hashnode.com/', { waitUntil: 'domcontentloaded', timeout: 45_000 });
        await page.waitForTimeout(3_000);
      }

      await page.goto('https://hashnode.com/draft/new', { waitUntil: 'domcontentloaded', timeout: 45_000 });
      const editorReady = await page.waitForSelector('textarea[placeholder*="title" i]', { state: 'visible', timeout: 20_000 }).then(() => true).catch(() => false);
      if (!editorReady) {
        const write = page.locator('button:has-text("Write"), a[href*="/draft/new"], a:has-text("Write")').first();
        await write.waitFor({ state: 'visible', timeout: 15_000 });
        await write.click({ force: true });
        await page.waitForSelector('textarea[placeholder*="title" i]', { state: 'visible', timeout: 30_000 });
      }
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new ComposerError(this.platform, detail);
    }
  }

  async createPost(page: Page, post: PublishPost): Promise<void> {
    try {
      const title = page.locator('textarea[placeholder*="title" i]').first();
      await title.waitFor({ state: 'visible', timeout: 10_000 });
      await title.fill(post.text.split('\n')[0].slice(0, 120));
      await page.waitForTimeout(500);

      const body = page.locator('.ProseMirror[contenteditable="true"], [contenteditable="true"]').last();
      await body.waitFor({ state: 'visible', timeout: 10_000 });
      await body.click();
      await page.keyboard.press('Control+A');
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
      const publishButton = page.locator('button:has-text("Publish")').first();
      await publishButton.waitFor({ state: 'visible', timeout: 15_000 });
      await publishButton.click({ force: true });
      await page.waitForTimeout(2_000);

      const confirm = page.locator('[role="dialog"] button:has-text("Publish"), button:has-text("Publish now")').last();
      if (await confirm.isVisible().catch(() => false)) {
        await confirm.click({ force: true });
      }

      await page.waitForURL((url) => !url.pathname.startsWith('/draft'), { timeout: 45_000 }).catch(() => {});
      await page.waitForTimeout(3_000);
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new PublishError(this.platform, detail);
    }
  }

  async verifyPublished(page: Page): Promise<{ success: boolean; postUrl?: string }> {
    try {
      await page.waitForTimeout(3_000);
      const url = page.url().split('?')[0];
      if (url.includes('/draft')) {
        return { success: false };
      }
      await page.goto('https://hashnode.com/', { waitUntil: 'domcontentloaded', timeout: 30_000 }).catch(() => {});
      await page.waitForTimeout(3_000);
      const blogUrl = await page.evaluate(() => {
        const link = Array.from(document.querySelectorAll('a[href]')).find(anchor => /^https?:\/\/[^/]+\.hashnode\.dev\/?$/.test((anchor as HTMLAnchorElement).href));
        return link ? (link as HTMLAnchorElement).href : '';
      });
      if (!blogUrl) {
        return { success: true, postUrl: url };
      }
      await page.goto(blogUrl, { waitUntil: 'domcontentloaded', timeout: 30_000 }).catch(() => {});
      await page.waitForTimeout(3_000);
      const postUrl = await page.evaluate((origin: string) => {
        const reserved = new Set(['archive', 'newsletter', 'series', 'tags', 'badges', 'sponsor', 'about', 'members']);
        const link = Array.from(document.querySelectorAll('a[href]')).find(anchor => {
          const href = (anchor as HTMLAnchorElement).href;
          const slug = href.startsWith(origin) ? href.slice(origin.length + 1) : '';
          return /^[a-z0-9-]+$/.test(slug) && !reserved.has(slug);
        });
        return link ? (link as HTMLAnchorElement).href : undefined;
      }, blogUrl.replace(/\/$/, ''));
      return { success: true, postUrl: postUrl ?? url };
    } catch {
      return { success: false };
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
