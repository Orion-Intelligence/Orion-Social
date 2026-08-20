const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launchPersistentContext('/home/marij-hashmi/Desktop/orion/Orion-Social/social-automation/profiles/default/facebook', { headless: true, args: ['--disable-blink-features=AutomationControlled'] });
  const page = browser.pages()[0] || await browser.newPage();
  await page.goto('https://www.facebook.com/', { waitUntil: 'networkidle', timeout: 30000 });
  const url = page.url();
  const html = await page.content();
  console.log("URL:", url);
  console.log("HTML snippet:", html.substring(0, 500));
  await page.screenshot({ path: 'fb.png' });
  const profileLink = await page.$('[aria-label="Your profile"], [data-pagelet="ProfileTail"]');
  const navBar = await page.$('[role="navigation"]');
  console.log("ProfileLink:", !!profileLink, "NavBar:", !!navBar);
  const cookieBanner = await page.$('[data-cookiebanner="accept_button"]');
  console.log("Cookie Banner:", !!cookieBanner);
  await browser.close();
})();
