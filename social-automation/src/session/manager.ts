import path from 'node:path';
import fs from 'node:fs';
import { chromium } from 'playwright';
import type { Browser, BrowserContext, Page } from 'playwright';

import { Config } from '../config.js';
import { logger } from '../logger.js';
import {
  BrowserLaunchError,
  ProfileNotFoundError,
  SessionExpiredError,
} from '../errors.js';
import { getPlatform } from '../platforms/registry.js';
import type { SessionStatus } from '../platforms/types.js';

// ---------------------------------------------------------------------------
// Browser lifecycle
// ---------------------------------------------------------------------------

/**
 * Launch Chromium with optional persistent profile.
 *
 * When `userDataDir` is provided Playwright uses `launchPersistentContext`
 * which persists cookies, localStorage, and IndexedDB across sessions.
 */
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


// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Helper to find the latest session file for a platform
 */
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

/**
 * Launch an ephemeral browser context loaded with the session cookies.
 *
 * @throws {ProfileNotFoundError} if no session file exists.
 * @throws {SessionExpiredError} if the stored session is no longer valid.
 */
export async function getSocialContext(
  platformName: string,
  userId: string = 'default'
): Promise<BrowserContext> {
  const platform = getPlatform(platformName);
  const sessionPath = findSessionFile(platform.name);

  if (!sessionPath) {
    throw new ProfileNotFoundError(platform.name, 'sessions folder');
  }

  logger.info(`Loading session for ${platform.displayName} (User: ${userId})`);

  // Load and sanitize cookies
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

  const browser = await launchBrowser(platform.name, { headless: Config.headless });
  const context = await browser.newContext({ viewport: null });
  await context.addCookies(sanitizedCookies);

  // Monkey-patch context.close to also close the browser
  const originalClose = context.close.bind(context);
  context.close = async () => {
    await originalClose();
    await browser.close();
  };

  // Verify the session is still valid.
  try {
    const page = context.pages()[0] ?? await context.newPage();
    const valid = await platform.isAuthenticated(page);
    if (!valid) {
      throw new SessionExpiredError(platform.name);
    }
    return context;
  } catch (err) {
    await safeClose(context);
    throw err;
  }
}

/**
 * Convenience wrapper: open context and return its first page.
 * Caller is responsible for closing the context via `page.context().close()`.
 */
export async function getSocialPage(
  platformName: string,
): Promise<Page> {
  const context = await getSocialContext(platformName);
  return context.pages()[0] ?? await context.newPage();
}

/**
 * Convenience wrapper: launch a full browser bound to the platform profile.
 * Returns the browser instance. Caller manages its lifecycle.
 */
export async function getSocialBrowser(
  platformName: string,
): Promise<Browser> {
  // Validate platform first.
  getPlatform(platformName);
  return launchBrowser(platformName, { headless: Config.headless });
}

/**
 * Retrieve safe session-status information for a platform.
 * Never exposes cookies, tokens, or credentials.
 */
export async function getSessionStatus(
  platformName: string,
  userId: string = 'default'
): Promise<SessionStatus> {
  const platform = getPlatform(platformName);
  const sessionPath = findSessionFile(platform.name);
  const configured = sessionPath !== null;

  let authenticated = false;
  if (configured) {
    let context: BrowserContext | null = null;
    try {
      context = await getSocialContext(platformName, userId);
      // If getSocialContext succeeds, it means it's authenticated.
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

// ---------------------------------------------------------------------------
// External Session Injection (Extension Integration)
// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

/** Close a browser context, swallowing errors during shutdown. */
async function safeClose(context: BrowserContext): Promise<void> {
  try {
    await context.close();
  } catch (err: unknown) {
    logger.warn('Error closing browser context', {
      error: err instanceof Error ? err.message : String(err),
    });
  }
}
