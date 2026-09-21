import type { Page } from 'playwright';
import type { SocialPlatform } from '../../shared/model/models.js';

export class TikTokPlatform implements SocialPlatform {
  readonly name = 'tiktok';
  readonly displayName = 'TikTok';
  readonly loginUrl = 'https://www.tiktok.com/login';

  async isAuthenticated(page: Page, navigate = true): Promise<boolean> {
    try {
      if (navigate) {
        await page.goto('https://www.tiktok.com/foryou', {
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
      const hasAuthCookie = cookies.some(c => c.name === 'sessionid' && c.value !== '');

      const authenticated = await page.evaluate(() => {
        const passwordInput = document.querySelector('input[type="password"]');
        if (passwordInput) {
          return false;
        }
        const marker = document.querySelector('[data-e2e="profile-icon"], [data-e2e="nav-profile"], [data-e2e="upload-icon"]');
        return marker !== null;
      });

      return authenticated || hasAuthCookie;
    } catch {
      return false;
    }
  }
}
