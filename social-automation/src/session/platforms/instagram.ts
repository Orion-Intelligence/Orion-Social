import type { Page } from 'playwright';
import type { SocialPlatform } from '../../shared/model/models.js';

export class InstagramPlatform implements SocialPlatform {
  readonly name = 'instagram';
  readonly displayName = 'Instagram';
  readonly loginUrl = 'https://www.instagram.com/accounts/login/';

  async isAuthenticated(page: Page, navigate = true): Promise<boolean> {
    try {
      if (navigate) {
        await page.goto('https://www.instagram.com/', {
          waitUntil: 'domcontentloaded',
          timeout: 15_000,
        });
      }

      const authenticated = await page.evaluate(() => {
        const url = window.location.href;
        
        if (url.includes('/accounts/login')) {
          return false;
        }
        
        const navProfile = document.querySelector('a[href*="/direct/"] , svg[aria-label="Home"]');
        const createIcon = document.querySelector('svg[aria-label="New post"]');
        
        const navBar = document.querySelector('nav[role="navigation"]');
        return navProfile !== null || createIcon !== null || navBar !== null;
      });

      return authenticated;
    } catch {
      return false;
    }
  }
}
