import type { Page } from 'playwright';
import type { SocialPlatform } from '../../shared/model/models.js';

export class BehancePlatform implements SocialPlatform {
  readonly name = 'behance';
  readonly displayName = 'Behance';
  readonly loginUrl = 'https://www.behance.net/login';

  async isAuthenticated(page: Page, navigate = true): Promise<boolean> {
    try {
      if (navigate) {
        await page.goto('https://www.behance.net/', {
          waitUntil: 'domcontentloaded',
          timeout: 45_000,
        });
      }
      await page.waitForLoadState('networkidle', { timeout: 15_000 }).catch(() => {});
      await page.waitForTimeout(1_500);

      const url = page.url();
      if (url.includes('auth.services.adobe.com') || url.includes('/login')) {
        return false;
      }

      const cookies = await page.context().cookies();
      const hasAuthCookie = cookies.some(c => (c.name === 'bims_sid' || c.name === 'ims_sid') && c.value !== '');

      const authenticated = await page.evaluate(() => {
        const passwordInput = document.querySelector('input[type="password"]');
        if (passwordInput) {
          return false;
        }
        const marker = document.querySelector('[data-testid="user-avatar"], a[href*="/portfolio/editor"], [class*="UserMenu"]');
        return marker !== null;
      });

      return authenticated || hasAuthCookie;
    } catch {
      return false;
    }
  }
}
