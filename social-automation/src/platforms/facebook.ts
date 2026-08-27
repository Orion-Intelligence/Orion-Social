import type { Page } from 'playwright';
import type { SocialPlatform } from './types.js';

export class FacebookPlatform implements SocialPlatform {
  readonly name = 'facebook';
  readonly displayName = 'Facebook';
  readonly loginUrl = 'https://www.facebook.com/login';

  async isAuthenticated(page: Page, navigate = true): Promise<boolean> {
    try {
      if (navigate) {
        await page.goto('https://www.facebook.com/', {
          waitUntil: 'domcontentloaded',
          timeout: 15_000,
        });
      }

      const cookies = await page.context().cookies();
      const hasCUser = cookies.some(c => c.name === 'c_user');
      
      if (hasCUser) {
        return true;
      }

      const authenticated = await page.evaluate(() => {
        const url = window.location.href;
        if (url.includes('/login') || url.includes('/reg') || url.includes('/r.php')) {
          return false;
        }
        const emailInput = document.querySelector('input[name="email"]');
        const passInput = document.querySelector('input[name="pass"]');
        if (emailInput || passInput) {
          return false;
        }
        const profileLink = document.querySelector('[aria-label="Your profile"], [data-pagelet="ProfileTail"]');
        const navBar = document.querySelector('[role="navigation"]');
        return profileLink !== null || navBar !== null;
      });

      return authenticated;
    } catch {
      return false;
    }
  }
}
