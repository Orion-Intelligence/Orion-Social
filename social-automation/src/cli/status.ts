#!/usr/bin/env node
/**
 * CLI: check social-platform session status.
 *
 * Usage:
 *   npm run social:status                          # Show all platforms
 *   npm run social:status -- --platform facebook   # Show single platform
 *
 * Output contains ONLY safe information (no cookies, tokens, or credentials).
 */

import { getSessionStatus } from '../session/manager.js';
import { listPlatforms } from '../platforms/registry.js';
import { SocialAutomationError } from '../errors.js';
import { logger } from '../logger.js';

function parseArgs(argv: string[]): { platform: string | null; userId: string } {
  let platform = null;
  const pIdx = argv.indexOf('--platform');
  if (pIdx !== -1 && pIdx + 1 < argv.length) {
    platform = argv[pIdx + 1] ?? '';
  }
  
  let userId = 'default';
  const uIdx = argv.indexOf('--user');
  if (uIdx !== -1 && uIdx + 1 < argv.length) {
    userId = argv[uIdx + 1] ?? 'default';
  }

  return { platform, userId };
}

async function showSinglePlatform(platform: string, userId: string): Promise<void> {
  const status = await getSessionStatus(platform, userId);

  console.log('\n— Session Status —');
  console.log(`  Platform:      ${status.platform}`);
  console.log(`  Authenticated: ${status.authenticated ? 'yes' : 'no'}`);
  console.log(`  Profile:       ${status.profileConfigured ? 'configured' : 'not configured'}`);
  console.log(`  Profile path:  ${status.profilePath}`);

  if (status.profileConfigured && !status.authenticated) {
    console.log(`\n⚠ Session is expired or invalid.`);
  }
}

async function showAllPlatforms(userId: string): Promise<void> {
  const platforms = listPlatforms();

  console.log(`\n— Session Status (All Platforms, User: ${userId}) —\n`);

  // Table header.
  const header = 'Platform'.padEnd(16) + 'Authenticated';
  console.log(header);
  console.log('─'.repeat(header.length));

  for (const name of platforms) {
    try {
      const status = await getSessionStatus(name, userId);
      const authText = status.authenticated ? 'yes' : 'no';
      console.log(`${status.platform.padEnd(16)}${authText}`);
    } catch {
      console.log(`${name.padEnd(16)}error`);
    }
  }

  console.log('');
}

async function main(): Promise<void> {
  const { platform, userId } = parseArgs(process.argv);

  try {
    if (platform) {
      await showSinglePlatform(platform, userId);
    } else {
      await showAllPlatforms(userId);
    }
  } catch (err: unknown) {
    if (err instanceof SocialAutomationError) {
      logger.error(err.message, { code: err.code });
    } else {
      logger.error('Unexpected error checking status', {
        error: err instanceof Error ? err.message : String(err),
      });
    }
    process.exit(1);
  }
}

main();
