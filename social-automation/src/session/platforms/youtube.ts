import type { Page } from 'playwright';
import type { SocialPlatform } from '../../shared/model/models.js';

export class YouTubePlatform implements SocialPlatform {
  readonly name = 'youtube';
  readonly displayName = 'YouTube';
  readonly loginUrl = 'https://accounts.google.com/ServiceLogin?service=youtube';

  async isAuthenticated(page: Page, navigate = true): Promise<boolean> {
    try {
      if (navigate) {
        await page.goto('https://www.youtube.com/', {
          waitUntil: 'domcontentloaded',
          timeout: 45_000,
        });
      }
      await page.waitForLoadState('networkidle', { timeout: 15_000 }).catch(() => {});
      await page.waitForTimeout(1_500);

      const url = page.url();
      if (url.includes('accounts.google.com')) {
        return false;
      }

      const cookies = await page.context().cookies();
      const hasAuthCookie = cookies.some(c => c.name === 'SAPISID' && c.value !== '');

      const authenticated = await page.evaluate(() => {
        const passwordInput = document.querySelector('input[type="password"]');
        if (passwordInput) {
          return false;
        }
        const marker = document.querySelector('#avatar-btn, ytd-topbar-menu-button-renderer #avatar-btn');
        return marker !== null;
      });

      return authenticated || hasAuthCookie;
    } catch {
      return false;
    }
  }
}
