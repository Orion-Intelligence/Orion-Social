import type { Page } from 'playwright';
import type { SocialPlatform } from '../../shared/model/models.js';

export class QuoraPlatform implements SocialPlatform {
  readonly name = 'quora';
  readonly displayName = 'Quora';
  readonly loginUrl = 'https://www.quora.com/';

  async isAuthenticated(page: Page, navigate = true): Promise<boolean> {
    try {
      if (navigate) {
        await page.goto('https://www.quora.com/', {
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
      const hasAuthCookie = cookies.some(c => c.name === 'm-b' && c.value !== '');

      const authenticated = await page.evaluate(() => {
        const passwordInput = document.querySelector('input[type="password"]');
        if (passwordInput) {
          return false;
        }
        const marker = document.querySelector('a[href*="/profile/"] img, [class*="profile_photo" i] img, button[aria-label*="Add question" i]');
        return marker !== null;
      });

      return authenticated || hasAuthCookie;
    } catch {
      return false;
    }
  }
}
