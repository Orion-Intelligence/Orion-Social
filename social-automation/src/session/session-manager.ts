import path from 'node:path';
import fs from 'node:fs';
import { chromium } from 'playwright';
import type { Browser, BrowserContext } from 'playwright';

import { Config } from '../shared/config.js';

import {
  BrowserLaunchError,
  ProfileNotFoundError,
  SessionExpiredError,
} from '../shared/errors.js';
import { getPlatform } from './platforms/registry.js';
import { DEFAULT_USER_AGENT } from './constants/constants.js';

async function launchBrowser(platformName: string, options: { headless: boolean }): Promise<Browser> {
  try {
    const args = platformName.toLowerCase() === 'x' 
      ? ['--disable-blink-features=AutomationControlled'] 
      : [];

    return await chromium.launch({
      headless: options.headless,
      args,
    });
  } catch (err: unknown) {
    const reason = err instanceof Error ? err.message : String(err);
    throw new BrowserLaunchError(reason);
  }
}

function findSessionFile(platformName: string): string | null {
  const sessionsDir = Config.sessionsBaseDir;
  if (!fs.existsSync(sessionsDir)) return null;
  
  const entries = fs.readdirSync(sessionsDir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.isDirectory() && entry.name.toLowerCase().startsWith(platformName.toLowerCase() + '-')) {
      const sessionPath = path.join(sessionsDir, entry.name, 'session.json.injected');
      if (fs.existsSync(sessionPath)) return sessionPath;
      const uninjPath = path.join(sessionsDir, entry.name, 'session.json');
      if (fs.existsSync(uninjPath)) return uninjPath;
    }
  }
  return null;
}

export async function getSocialContext(platformName: string, _userId: string = 'default', sessionFile?: string): Promise<BrowserContext> {
  const platform = getPlatform(platformName);
  const sessionPath = sessionFile || findSessionFile(platform.name);

  if (!sessionPath) {
    throw new ProfileNotFoundError(platform.name, 'sessions folder');
  }


  const content = fs.readFileSync(sessionPath, 'utf-8');
  let cookies = JSON.parse(content);
  if (!Array.isArray(cookies)) {
    if (cookies && Array.isArray(cookies.cookies)) cookies = cookies.cookies;
    else throw new Error('Invalid cookie format');
  }
  
  const sanitizedCookies = (cookies as Array<Record<string, unknown>>).map((c) => {
    const cookie: Record<string, unknown> = { ...c };
    if (cookie.sameSite && typeof cookie.sameSite === 'string') {
      const s = cookie.sameSite.toLowerCase();
      if (s === 'strict') cookie.sameSite = 'Strict';
      else if (s === 'lax') cookie.sameSite = 'Lax';
      else if (s === 'none') cookie.sameSite = 'None';
      else delete cookie.sameSite;
    } else {
      delete cookie.sameSite;
    }
    if (cookie.expires === -1 || cookie.expires === "") {
      delete cookie.expires;
    }
    return cookie;
  });

  const browser = await launchBrowser(platform.name, { headless: Config.headless });
  const context = await browser.newContext({
    viewport: null,
    userAgent: DEFAULT_USER_AGENT
  });
  await context.addCookies(sanitizedCookies as unknown as Parameters<typeof context.addCookies>[0]);

  const originalClose = context.close.bind(context);
  context.close = async () => {
    await originalClose();
    await browser.close();
  };

  let valid: boolean;
  try {
    const page = context.pages()[0] ?? await context.newPage();
    valid = await platform.isAuthenticated(page);
  } catch (err) {
    await safeClose(context);
    throw err;
  }

  if (!valid) {
    await safeClose(context);
    throw new SessionExpiredError(platform.name);
  }

  return context;
}

async function safeClose(context: BrowserContext): Promise<void> {
  try {
    await context.close();
  } catch {
    // ignore errors while closing the browser context during cleanup
  }
}
