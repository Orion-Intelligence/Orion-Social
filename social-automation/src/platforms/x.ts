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
        // Wait for React to mount the SPA
        await page.waitForTimeout(3_000);
      }

      const authenticated = await page.evaluate(() => {
        const url = window.location.href;
        // Unauthenticated users are redirected to the login flow.
        if (url.includes('/i/flow/login') || url.includes('/login')) {
          return false;
        }
        // Authenticated users see the compose-tweet button and navigation sidebar.
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
