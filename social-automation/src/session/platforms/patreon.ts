import type { Page } from 'playwright';
import type { SocialPlatform } from '../../shared/model/models.js';

export class PatreonPlatform implements SocialPlatform {
  readonly name = 'patreon';
  readonly displayName = 'Patreon';
  readonly loginUrl = 'https://www.patreon.com/login';

  async isAuthenticated(page: Page, navigate = true): Promise<boolean> {
    try {
      if (navigate) {
        await page.goto('https://www.patreon.com/home', {
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
      const hasAuthCookie = cookies.some(c => c.name === 'session_id' && c.value !== '');

      const authenticated = await page.evaluate(() => {
        const passwordInput = document.querySelector('input[type="password"]');
        if (passwordInput) {
          return false;
        }
        const marker = document.querySelector('[data-tag="user-menu"], [data-tag="navbar-profile"], img[alt*="avatar" i]');
        return marker !== null;
      });

      return authenticated || hasAuthCookie;
    } catch {
      return false;
    }
  }
}
