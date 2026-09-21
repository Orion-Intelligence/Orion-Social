import path from 'node:path';
import fs from 'node:fs';
import { chromium, firefox } from 'playwright';
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
    if (Config.browser === 'firefox') {
      return await firefox.launch({ headless: options.headless });
    }
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
  const state = JSON.parse(content);
  let cookies = state;
  if (!Array.isArray(cookies)) {
    if (cookies && Array.isArray(cookies.cookies)) cookies = cookies.cookies;
    else throw new Error('Invalid cookie format');
  }
  const userAgent = typeof state?.userAgent === 'string' && state.userAgent.trim() ? state.userAgent.trim() : DEFAULT_USER_AGENT;
  const localStorageEntries: Record<string, string> = state?.localStorage && typeof state.localStorage === 'object' ? state.localStorage : {};
  const storageOrigin = typeof state?.origin === 'string' ? state.origin : '';
  
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
    viewport: { width: 1366, height: 900 },
    userAgent,
  });
  await context.addCookies(sanitizedCookies as unknown as Parameters<typeof context.addCookies>[0]);
  if (storageOrigin && Object.keys(localStorageEntries).length > 0) {
    await context.addInitScript(({ origin, entries }: { origin: string; entries: Record<string, string> }) => {
      if (window.location.origin !== origin || window.localStorage.getItem('__orion_restored__')) return;
      for (const [key, value] of Object.entries(entries)) {
        try { window.localStorage.setItem(key, typeof value === 'string' ? value : JSON.stringify(value)); } catch { /* storage may be unavailable */ }
      }
      window.localStorage.setItem('__orion_restored__', '1');
    }, { origin: storageOrigin, entries: localStorageEntries });
  }

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
