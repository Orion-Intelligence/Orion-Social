import path from 'node:path';
import fs from 'node:fs';
import { chromium } from 'playwright';
import type { Browser, BrowserContext, Page } from 'playwright';

import { Config } from '../shared/config.js';

import {
  BrowserLaunchError,
  ProfileNotFoundError,
  SessionExpiredError,
} from '../shared/errors.js';
import { getPlatform } from './platforms/registry.js';
import type { SessionStatus } from '../shared/model/models.js';

async function launchBrowser(
  platformName: string,
  options: { headless: boolean }
): Promise<Browser> {
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

export async function getSocialContext(
  platformName: string,
  _userId: string = 'default',
  sessionFile?: string
): Promise<BrowserContext> {
  const platform = getPlatform(platformName);
  const sessionPath = sessionFile || findSessionFile(platform.name);

  if (!sessionPath) {
    throw new ProfileNotFoundError(platform.name, 'sessions folder');
  }

  console.log(`[Session] Loading session for ${platform.displayName}`);

  const content = fs.readFileSync(sessionPath, 'utf-8');
  let cookies = JSON.parse(content);
  if (!Array.isArray(cookies)) {
    if (cookies && Array.isArray(cookies.cookies)) cookies = cookies.cookies;
    else throw new Error('Invalid cookie format');
  }
  
  const sanitizedCookies = cookies.map((c: any) => {
    const cookie: any = { ...c };
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

  console.log(`[Session] Launching browser (${sanitizedCookies.length} cookies)`);
  const browser = await launchBrowser(platform.name, { headless: Config.headless });
  const context = await browser.newContext({ 
    viewport: null,
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
  });
  await context.addCookies(sanitizedCookies);

  const originalClose = context.close.bind(context);
  context.close = async () => {
    await originalClose();
    await browser.close();
  };

  try {
    const page = context.pages()[0] ?? await context.newPage();
    console.log(`[Session] Verifying session is still signed in`);
    const valid = await platform.isAuthenticated(page);
    if (!valid) {
      console.log(`[Session] Session is expired or signed out`);
      throw new SessionExpiredError(platform.name);
    }
    console.log(`[Session] Session verified, signed in`);
    return context;
  } catch (err) {
    await safeClose(context);
    throw err;
  }
}

export async function getSocialPage(
  platformName: string,
  _userId: string = 'default',
  sessionFile?: string
): Promise<Page> {
  const context = await getSocialContext(platformName, _userId, sessionFile);
  return context.pages()[0] ?? await context.newPage();
}

export async function getSocialBrowser(
  platformName: string,
): Promise<Browser> {
  
  getPlatform(platformName);
  return launchBrowser(platformName, { headless: Config.headless });
}

export async function getSessionStatus(
  platformName: string,
  _userId: string = 'default',
  sessionFile?: string
): Promise<SessionStatus> {
  const platform = getPlatform(platformName);
  const sessionPath = sessionFile || findSessionFile(platform.name);
  const configured = sessionPath !== null;

  let authenticated = false;
  if (configured) {
    let context: BrowserContext | null = null;
    try {
      context = await getSocialContext(platformName, _userId, sessionFile);
      
      authenticated = true;
    } catch {
      authenticated = false;
    } finally {
      if (context) {
        await safeClose(context);
      }
    }
  }

  return {
    platform: platform.displayName,
    authenticated,
    profileConfigured: configured,
    profilePath: sessionPath || 'Not found',
  };
}

async function safeClose(context: BrowserContext): Promise<void> {
  try {
    await context.close();
  } catch (err: unknown) {

  }
}
