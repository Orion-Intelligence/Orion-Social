import type { Page } from 'playwright';
import type { SocialPlatform } from '../../shared/model/models.js';

export class RedditPlatform implements SocialPlatform {
  readonly name = 'reddit';
  readonly displayName = 'Reddit';
  readonly loginUrl = 'https://www.reddit.com/login';

  async isAuthenticated(page: Page, navigate = true): Promise<boolean> {
    try {
      if (navigate) {
        await page.goto('https://www.reddit.com/', {
          waitUntil: 'domcontentloaded',
          timeout: 45_000,
        });
      }
      await page.waitForLoadState('networkidle', { timeout: 15_000 }).catch(() => {});
      await page.waitForTimeout(1_500);

      const url = page.url();
      if (url.includes('/login')) {
        return false;
      }

      const cookies = await page.context().cookies();
      const hasAuthCookie = cookies.some(c => c.name === 'reddit_session' && c.value !== '');

      const authenticated = await page.evaluate(() => {
        const passwordInput = document.querySelector('input[type="password"]');
        if (passwordInput) {
          return false;
        }
        const marker = document.querySelector('#expand-user-drawer-button, a[href="/submit"], faceplate-dropdown-menu');
        return marker !== null;
      });

      return authenticated || hasAuthCookie;
    } catch {
      return false;
    }
  }
}
