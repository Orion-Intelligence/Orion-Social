import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const PACKAGE_ROOT = path.resolve(__dirname, '..');

export const Config = Object.freeze({
  
  sessionsBaseDir: process.env['ORION_SOCIAL_SESSIONS_DIR']
    ?? path.join(PACKAGE_ROOT, '..', 'sessions'),

  headless: (process.env['ORION_SOCIAL_HEADLESS'] ?? 'true').toLowerCase() === 'true',

  loginTimeoutMs: Number(process.env['ORION_SOCIAL_LOGIN_TIMEOUT_MS'] ?? 300_000),

  authPollIntervalMs: Number(process.env['ORION_SOCIAL_AUTH_POLL_MS'] ?? 3_000),

  navigationTimeoutMs: Number(process.env['ORION_SOCIAL_NAV_TIMEOUT_MS'] ?? 30_000),
});

export type SocialConfig = typeof Config;
