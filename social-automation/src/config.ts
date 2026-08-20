import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/** Root of the social-automation package (one level above src/) */
const PACKAGE_ROOT = path.resolve(__dirname, '..');

/**
 * Centralised configuration for the social-automation module.
 *
 * Every value is resolved once at import-time from env vars with sensible
 * defaults so that callers never need to handle undefined.
 */
export const Config = Object.freeze({
  /**
   * Base directory that holds the raw sessions extracted by the extension.
   * Structure:  <sessionsBaseDir>/<platform>-<id>-session/session.json
   */
  sessionsBaseDir: process.env['ORION_SOCIAL_SESSIONS_DIR']
    ?? path.join(PACKAGE_ROOT, '..', 'sessions'),

  /** When true the browser launches without a visible window. */
  headless: (process.env['ORION_SOCIAL_HEADLESS'] ?? 'false').toLowerCase() === 'true',

  /**
   * Maximum time (ms) to wait for login-related navigations before giving up.
   * Generous default because manual MFA can be slow.
   */
  loginTimeoutMs: Number(process.env['ORION_SOCIAL_LOGIN_TIMEOUT_MS'] ?? 300_000),

  /** Interval (ms) between successive authentication-state polls during login. */
  authPollIntervalMs: Number(process.env['ORION_SOCIAL_AUTH_POLL_MS'] ?? 3_000),

  /** Navigation timeout (ms) for reuse / status checks. */
  navigationTimeoutMs: Number(process.env['ORION_SOCIAL_NAV_TIMEOUT_MS'] ?? 30_000),
});

export type SocialConfig = typeof Config;
