import fs from 'node:fs';

import { SocialAutomationError } from './errors.js';
import type { AutomationResult } from './model/models.js';

export function parseResultFileArg(argv: readonly string[]): string | undefined {
  const args = argv.slice(2);
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--result-file' && args[i + 1]) {
      return args[i + 1];
    }
  }
  return undefined;
}

export function writeResult(filePath: string | undefined, result: AutomationResult): void {
  if (!filePath) return;
  try {
    fs.writeFileSync(filePath, JSON.stringify(result), 'utf-8');
  } catch (err: unknown) {
  }
}

export function isSessionExpiredCode(code: string | undefined): boolean {
  return code === 'SESSION_EXPIRED' || code === 'AUTHENTICATION_FAILED';
}

export function isSessionExpired(err: unknown): boolean {
  return err instanceof SocialAutomationError && isSessionExpiredCode(err.code);
}

export function errorReason(err: unknown): string {
  return err instanceof Error ? err.message : String(err);
}
