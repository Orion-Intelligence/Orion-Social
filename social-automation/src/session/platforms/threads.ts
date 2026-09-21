import type { Page } from 'playwright';
import type { SocialPlatform } from '../../shared/model/models.js';

export class ThreadsPlatform implements SocialPlatform {
  readonly name = 'threads';
  readonly displayName = 'Threads';
  readonly loginUrl = 'https://www.threads.com/login';

  async isAuthenticated(page: Page, navigate = true): Promise<boolean> {
    try {
      if (navigate) {
        await page.goto('https://www.threads.com/', {
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
        const marker = document.querySelector('svg[aria-label="Profile"], svg[aria-label="Create"], a[href*="/@"] img');
        return marker !== null;
      });

      return authenticated || hasAuthCookie;
    } catch {
      return false;
    }
  }
}
