import type { Page } from 'playwright';
import type { SocialPlatform } from '../../shared/model/models.js';

export class OkRuPlatform implements SocialPlatform {
  readonly name = 'okru';
  readonly displayName = 'OK.ru';
  readonly loginUrl = 'https://ok.ru/dk?st.cmd=anonymMain';

  async isAuthenticated(page: Page, navigate = true): Promise<boolean> {
    try {
      if (navigate) {
        await page.goto('https://ok.ru/', {
          waitUntil: 'domcontentloaded',
          timeout: 45_000,
        });
      }
      await page.waitForLoadState('networkidle', { timeout: 15_000 }).catch(() => {});
      await page.waitForTimeout(1_500);

      const url = page.url();
      if (url.includes('st.cmd=anonymMain') || url.includes('st.cmd=anonymLogin')) {
        return false;
      }

      const cookies = await page.context().cookies();
      const hasAuthCookie = cookies.some(c => c.name === 'AUTHCODE' && c.value !== '');

      const authenticated = await page.evaluate(() => {
        const passwordInput = document.querySelector('input[type="password"]');
        if (passwordInput) {
          return false;
        }
        const marker = document.querySelector('[data-l*="t,userMain"], #hook_Block_Navigation, .toolbar_nav');
        return marker !== null;
      });

      return authenticated || hasAuthCookie;
    } catch {
      return false;
    }
  }
}
