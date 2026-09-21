import type { Page } from 'playwright';
import type { SocialPlatform } from '../../shared/model/models.js';

export class HashnodePlatform implements SocialPlatform {
  readonly name = 'hashnode';
  readonly displayName = 'Hashnode';
  readonly loginUrl = 'https://hashnode.com/onboard';

  async isAuthenticated(page: Page, navigate = true): Promise<boolean> {
    try {
      if (navigate) {
        await page.goto('https://hashnode.com/', {
          waitUntil: 'domcontentloaded',
          timeout: 45_000,
        });
      }
      await page.waitForLoadState('networkidle', { timeout: 15_000 }).catch(() => {});
      await page.waitForTimeout(1_500);

      const url = page.url();
      if (url.includes('/login') || url.includes('/signin')) {
        return false;
      }

      const cookies = await page.context().cookies();
      const authCookieNames = ['hashnode-session', '__Secure-authjs.session-token', 'authjs.session-token', 'jwt'];
      const hasAuthCookie = cookies.some(c => authCookieNames.includes(c.name) && c.value !== '');

      const authenticated = await page.evaluate(() => {
        const passwordInput = document.querySelector('input[type="password"]');
        if (passwordInput) {
          return false;
        }
        const marker = document.querySelector('a[href*="/drafts"], a[href*="/draft/new"], a[href*="/draft"], a[href="/write"], a[href*="hashnode.com/draft"]');
        return marker !== null;
      });

      return authenticated || hasAuthCookie;
    } catch {
      return false;
    }
  }
}
