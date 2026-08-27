import type { Page } from 'playwright';
import type { SocialPlatform } from './types.js';

export class LinkedInPlatform implements SocialPlatform {
  readonly name = 'linkedin';
  readonly displayName = 'LinkedIn';
  readonly loginUrl = 'https://www.linkedin.com/login';

  async isAuthenticated(page: Page, navigate = true): Promise<boolean> {
    try {
      if (navigate) {
        await page.goto('https://www.linkedin.com/feed/', {
          waitUntil: 'domcontentloaded',
          timeout: 15_000,
        });
      }

      const authenticated = await page.evaluate(() => {
        const url = window.location.href;
        
        if (url.includes('/login') || url.includes('/authwall') || url.includes('/signup') || url.includes('/checkpoint')) {
          return false;
        }
        
        const globalNav = document.querySelector('#global-nav, .global-nav, .global-nav__me');
        const feedIdentity = document.querySelector('.feed-identity-module, .scaffold-layout');
        const messaging = document.querySelector('a[href*="/messaging/"]');
        const profile = document.querySelector('a[href*="/in/"]');
        return globalNav !== null || feedIdentity !== null || messaging !== null || profile !== null;
      });

      return authenticated;
    } catch {
      return false;
    }
  }
}
