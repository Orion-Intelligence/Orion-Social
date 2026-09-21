import type { Page } from 'playwright';
import type { SocialPlatform } from '../../shared/model/models.js';

export class MeWePlatform implements SocialPlatform {
  readonly name = 'mewe';
  readonly displayName = 'MeWe';
  readonly loginUrl = 'https://mewe.com/login';

  async isAuthenticated(page: Page, navigate = true): Promise<boolean> {
    try {
      if (navigate) {
        await page.goto('https://mewe.com/myworld', {
          waitUntil: 'domcontentloaded',
          timeout: 45_000,
        });
      }
      await page.waitForLoadState('networkidle', { timeout: 15_000 }).catch(() => {});
      await page.waitForTimeout(1_500);

      const url = page.url();
      if (url.includes('/login') || url.includes('/register')) {
        return false;
      }

      const cookies = await page.context().cookies();
      const hasAuthCookie = cookies.some(c => c.name === 'session-id' && c.value !== '');

      const authenticated = await page.evaluate(() => {
        const passwordInput = document.querySelector('input[type="password"]');
        if (passwordInput) {
          return false;
        }
        const marker = document.querySelector('.c-mw-posts-feed, .c-mw-postbar, .mewe-app-content');
        return marker !== null;
      });

      return authenticated || hasAuthCookie;
    } catch {
      return false;
    }
  }
}
