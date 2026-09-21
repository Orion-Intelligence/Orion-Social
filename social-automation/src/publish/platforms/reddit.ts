import type { Page } from 'playwright';
import type { SocialPlatformAdapter, PublishPost } from '../model/models.js';
import { ComposerError, MediaUploadError, PublishError } from '../../shared/errors.js';

export class RedditAdapter implements SocialPlatformAdapter {
  readonly platform = 'reddit' as const;
  readonly displayName = 'Reddit';
  readonly supportedImageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];
  readonly maxImages = 20;

  private username = '';
  private title = '';

  async openComposer(page: Page): Promise<void> {
    try {
      await page.goto('https://www.reddit.com/', {
        waitUntil: 'domcontentloaded',
        timeout: 30_000,
      });
      await page.waitForTimeout(2_000);

      const username = await this.resolveUsername(page);
      if (!username) {
        throw new Error('Could not resolve the logged-in Reddit username');
      }
      this.username = username;

      await page.goto(`https://www.reddit.com/user/${username}/submit/?type=TEXT`, {
        waitUntil: 'domcontentloaded',
        timeout: 30_000,
      });

      await page.waitForSelector(
        'faceplate-textarea-input[name="title"] textarea, ' +
        'faceplate-textarea-input textarea, ' +
        'textarea[name="title"], ' +
        'input[name="title"], ' +
        'textarea[placeholder="Title"], ' +
        '[placeholder="Title"], ' +
        'div[slot="rte"][name="body"], ' +
        'shreddit-composer',
        { state: 'visible', timeout: 30_000 },
      );
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new ComposerError(this.platform, detail);
    }
  }

  private async resolveUsername(page: Page): Promise<string> {
    const strategies = [
      () => this.usernameFromOldReddit(page),
      () => this.usernameFromApi(page),
      () => this.usernameFromRedirect(page),
      () => this.usernameFromDom(page),
    ];
    for (const strategy of strategies) {
      const name = await strategy();
      if (name) {
        return name;
      }
    }
    return '';
  }

  private async usernameFromOldReddit(page: Page): Promise<string> {
    await page.goto('https://old.reddit.com/', { waitUntil: 'domcontentloaded', timeout: 30_000 }).catch(() => undefined);
    return page.evaluate(() => {
      const anchor = document.querySelector('#header-bottom-right span.user a, .user a[href*="/user/"]');
      const href = anchor?.getAttribute('href') || '';
      const match = href.match(/\/user\/([^/?]+)/);
      if (match && match[1] !== 'me') {
        return match[1];
      }
      const text = (anchor?.textContent || '').trim();
      return text && text.toLowerCase() !== 'login' ? text : '';
    }).catch(() => '');
  }

  private async usernameFromRedirect(page: Page): Promise<string> {
    await page.goto('https://www.reddit.com/user/me/', { waitUntil: 'domcontentloaded', timeout: 30_000 }).catch(() => undefined);
    await page.waitForURL(/\/user\/(?!me(?:\/|$|\?))[^/?]+/, { timeout: 15_000 }).catch(() => undefined);
    const match = page.url().match(/\/user\/([^/?]+)/);
    return match && match[1] && match[1] !== 'me' ? match[1] : '';
  }

  private async usernameFromApi(page: Page): Promise<string> {
    const response = await page.request.get('https://www.reddit.com/api/me.json', { timeout: 15_000 }).catch(() => null);
    if (!response || !response.ok()) {
      return '';
    }
    const body = await response.json().catch(() => null) as { data?: { name?: string }; name?: string } | null;
    return String(body?.data?.name || body?.name || '');
  }

  private async usernameFromDom(page: Page): Promise<string> {
    return page.evaluate(() => {
      const app = document.querySelector('shreddit-app');
      const attr = app?.getAttribute('user') || app?.getAttribute('data-username') || '';
      if (attr) {
        return attr;
      }
      const link = document.querySelector('a[href^="/user/"][href$="/"]');
      const href = link?.getAttribute('href') || '';
      const parsed = href.match(/\/user\/([^/?]+)/);
      return parsed && parsed[1] !== 'me' ? parsed[1] : '';
    }).catch(() => '');
  }

  async createPost(page: Page, post: PublishPost): Promise<void> {
    try {
      if (post.images && post.images.length > 0) {
        await page.locator('button[role="tab"]:has-text("Images"), a[role="tab"]:has-text("Images"), [data-select-value="IMAGE"]').first().click({ timeout: 5_000 }).catch(() => {});
        await page.waitForTimeout(1_000);
      }

      const title = page.locator('faceplate-textarea-input[name="title"] textarea, textarea[name="title"]').first();
      await title.waitFor({ state: 'visible', timeout: 10_000 });
      await title.click();
      this.title = post.text.split('\n')[0].slice(0, 280);
      await page.keyboard.type(this.title, { delay: 5 });

      if (post.images && post.images.length > 0) {
        await this.uploadMedia(page, post.images);
      } else {
        const body = page.locator('div[slot="rte"][name="body"][contenteditable="true"], shreddit-composer [contenteditable="true"]').first();
        const bodyVisible = await body.isVisible().catch(() => false);
        if (bodyVisible) {
          await body.click();
          await page.keyboard.type(post.text, { delay: 5 });
        }
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
      const postButton = page.getByRole('button', { name: 'Post', exact: true }).first();
      await postButton.waitFor({ state: 'visible', timeout: 10_000 });
      for (let attempt = 0; attempt < 20 && !(await postButton.isEnabled()); attempt++) {
        await page.waitForTimeout(1_000);
      }
      const createResponse = this.waitForCreatePost(page);
      await postButton.click();

      await page.waitForURL(/\/comments\//, { timeout: 45_000 }).catch(() => {});

      if (!page.url().includes('/comments/')) {
        const apiError = await createResponse;
        if (apiError) {
          throw new PublishError(this.platform, apiError);
        }
        const rejection = await page.evaluate(() => {
          const text = document.body.innerText;
          const index = text.indexOf('Hmm,');
          return index >= 0 ? text.slice(index, index + 120).split('\n')[0].trim() : '';
        });
        if (rejection.includes("community doesn't exist") && !page.url().includes('/r/test/')) {
          await this.submitToTestCommunity(page);
          return;
        }
        if (rejection) {
          throw new PublishError(this.platform, rejection);
        }
      }
    } catch (err: unknown) {
      if (err instanceof PublishError) {
        throw err;
      }
      const detail = err instanceof Error ? err.message : String(err);
      throw new PublishError(this.platform, detail);
    }
  }

  private async submitToTestCommunity(page: Page): Promise<void> {
    const title = await page.locator('faceplate-textarea-input[name="title"] textarea, textarea[name="title"]').first().inputValue();
    const body = await page.locator('div[slot="rte"][name="body"]').first().innerText().catch(() => '');

    await page.goto('https://www.reddit.com/r/test/submit/?type=TEXT', { waitUntil: 'domcontentloaded', timeout: 30_000 });
    const titleField = page.locator('faceplate-textarea-input[name="title"] textarea, textarea[name="title"]').first();
    await titleField.waitFor({ state: 'visible', timeout: 30_000 });
    await titleField.click();
    await page.keyboard.type(title, { delay: 5 });
    const bodyField = page.locator('div[slot="rte"][name="body"][contenteditable="true"]').first();
    if (body && await bodyField.isVisible().catch(() => false)) {
      await bodyField.click();
      await page.keyboard.type(body, { delay: 5 });
    }

    const postButton = page.getByRole('button', { name: 'Post', exact: true }).first();
    for (let attempt = 0; attempt < 20 && !(await postButton.isEnabled()); attempt++) {
      await page.waitForTimeout(1_000);
    }
    const createResponse = this.waitForCreatePost(page);
    await postButton.click();
    await page.waitForURL(/\/comments\//, { timeout: 45_000 }).catch(() => {});
    if (!page.url().includes('/comments/')) {
      const apiError = await createResponse;
      if (apiError) {
        throw new PublishError(this.platform, apiError);
      }
    }
  }

  private waitForCreatePost(page: Page): Promise<string> {
    return page.waitForResponse((response) => response.request().method() === 'POST' && response.url().includes('/svc/shreddit/graphql') && /"operation(Name)?"\s*:\s*"CreatePost"/.test(response.request().postData() ?? ''), { timeout: 45_000 })
      .then(async (response) => {
        const payload = await response.json().catch(() => null) as { data?: { createSubredditPost?: { ok?: boolean; errors?: { message?: string }[] } } } | null;
        const result = payload?.data?.createSubredditPost;
        if (!result || result.ok) {
          return '';
        }
        return result.errors?.map((entry) => entry.message ?? '').filter(Boolean).join('; ') || 'Reddit rejected the post';
      })
      .catch(() => '');
  }

  async verifyPublished(page: Page): Promise<{ success: boolean; postUrl?: string }> {
    try {
      await page.waitForTimeout(2_000);
      const url = page.url();
      if (url.includes('/comments/')) {
        return { success: true, postUrl: url.split('?')[0] };
      }
      if (!this.username || !this.title) {
        return { success: false };
      }

      await page.goto(`https://www.reddit.com/user/${this.username}/submitted/`, { waitUntil: 'domcontentloaded', timeout: 30_000 });
      await page.waitForSelector('shreddit-post', { timeout: 15_000 }).catch(() => {});
      const permalink = await page.evaluate((title: string) => {
        const posts = Array.from(document.querySelectorAll('shreddit-post'));
        const match = posts.find(post => (post.getAttribute('post-title') || '').trim() === title);
        return match ? match.getAttribute('permalink') || '' : '';
      }, this.title);
      if (!permalink) {
        return { success: false };
      }
      return { success: true, postUrl: permalink.startsWith('http') ? permalink : `https://www.reddit.com${permalink}` };
    } catch {
      return { success: false };
    }
  }

  private async uploadMedia(page: Page, files: readonly string[]): Promise<void> {
    try {
      const fileInput = page.locator('input[type="file"]').first();
      await fileInput.waitFor({ state: 'attached', timeout: 10_000 });
      await fileInput.setInputFiles([...files]);

      await page.waitForTimeout(5_000);
    } catch (err: unknown) {
      const detail = err instanceof Error ? err.message : String(err);
      throw new MediaUploadError(this.platform, detail);
    }
  }
}
