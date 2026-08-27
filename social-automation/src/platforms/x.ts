import type { Page } from 'playwright';
import type { SocialPlatform } from './types.js';

export class XPlatform implements SocialPlatform {
  readonly name = 'x';
  readonly displayName = 'X (Twitter)';
  readonly loginUrl = 'https://x.com/i/flow/login';

  async isAuthenticated(page: Page, navigate = true): Promise<boolean> {
    try {
      if (navigate) {
        await page.goto('https://x.com/home', {
          waitUntil: 'domcontentloaded',
          timeout: 15_000,
        });
        
        await page.waitForTimeout(3_000);
      }

      const authenticated = await page.evaluate(() => {
        const url = window.location.href;
        
        if (url.includes('/i/flow/login') || url.includes('/login')) {
          return false;
        }
        
        const composeTweet = document.querySelector('[data-testid="SideNav_NewTweet_Button"]');
        const accountSwitcher = document.querySelector('[data-testid="SideNav_AccountSwitcher_Button"]');
        return composeTweet !== null || accountSwitcher !== null;
      });

      return authenticated;
    } catch {
      return false;
    }
  }
}
