import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const PACKAGE_ROOT = path.resolve(__dirname, '..');

export const Config = Object.freeze({
  
  sessionsBaseDir: process.env['ORION_SOCIAL_SESSIONS_DIR']
    ?? path.join(PACKAGE_ROOT, '..', 'sessions'),

  headless: (process.env['ORION_SOCIAL_HEADLESS'] ?? 'true').toLowerCase() === 'true',

});

export type SocialConfig = typeof Config;
