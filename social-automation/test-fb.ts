import { chromium } from 'playwright';

(async () => {
  const browser = await chromium.launchPersistentContext('/home/marij-hashmi/Desktop/orion/Orion-Social/social-automation/profiles/default/facebook', { headless: true, args: ['--disable-blink-features=AutomationControlled'] });
  const page = browser.pages()[0] || await browser.newPage();
  await page.goto('https://www.facebook.com/', { waitUntil: 'networkidle', timeout: 30000 });
  const url = page.url();
  const html = await page.content();
  console.log("URL:", url);
  console.log("HTML snippet:", html.substring(0, 500));
  await page.screenshot({ path: 'fb.png' });
  const cookies = await browser.cookies();
  const cUser = cookies.find(c => c.name === 'c_user');
  console.log("c_user cookie:", !!cUser);
  await browser.close();
})();
