import fs from 'node:fs';

import { SocialAutomationError } from './errors.js';

export interface PostResult {
  post_url: string;
  error: boolean;
  error_reason: string;
  session_expired: boolean;
}

export interface DetectedAd {
  url: string;
  author: string;
  content_text: string;
  metadata: string;
  likes: string;
  shares: string;
  views: string;
  detected_at: string;
}

export interface AdDetectionResult {
  total_detected_ads: number;
  ads: DetectedAd[];
  error: boolean;
  error_reason: string;
  session_expired: boolean;
}

export function parseResultFileArg(argv: readonly string[]): string | undefined {
  const args = argv.slice(2);
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--result-file' && args[i + 1]) {
      return args[i + 1];
    }
  }
  return undefined;
}

export function writeResult(filePath: string | undefined, result: PostResult | AdDetectionResult): void {
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
