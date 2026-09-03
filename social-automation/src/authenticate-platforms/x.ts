import type { Page } from 'playwright';
import type { SocialPlatform } from '../types.js';

export class XPlatform implements SocialPlatform {
  readonly name = 'x';
  readonly displayName = 'X (Twitter)';
  readonly loginUrl = 'https://x.com/i/flow/login';

  async isAuthenticated(page: Page, navigate = true): Promise<boolean> {
    try {
      if (navigate) {
        await page.goto('https://x.com/home', {
          waitUntil: 'domcontentloaded',
          timeout: 30_000,
        });
      }

      await page.waitForFunction(() => {
        const url = window.location.href;
        if (url.includes('/i/flow/login') || url.includes('/login')) {
          return true;
        }
        const compose = document.querySelector('[data-testid="SideNav_NewTweet_Button"], [data-testid="AppTabBar_NewTweet_Button"]');
        const account = document.querySelector('[data-testid="SideNav_AccountSwitcher_Button"]');
        const homeNav = document.querySelector('[data-testid="AppTabBar_Home_Link"]');
        return compose !== null || account !== null || homeNav !== null;
      }, { timeout: 15_000 });

      const authenticated = await page.evaluate(() => {
        const url = window.location.href;
        if (url.includes('/i/flow/login') || url.includes('/login')) {
          return false;
        }
        return true;
      });

      return authenticated;
    } catch (err) {
      try {
        const url = page.url();
        if (url.includes('/i/flow/login') || url.includes('/login')) {
          return false;
        }
      } catch {}
      throw err;
    }
  }
}
