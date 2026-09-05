import type { SocialPlatform } from '../../shared/model/models.js';
import { FacebookPlatform } from './facebook.js';
import { XPlatform } from './x.js';
import { InstagramPlatform } from './instagram.js';
import { LinkedInPlatform } from './linkedin.js';
import { InvalidPlatformError } from '../../shared/errors.js';

const platforms: ReadonlyMap<string, SocialPlatform> = new Map<string, SocialPlatform>([
  ['facebook', new FacebookPlatform()],
  ['x', new XPlatform()],
  ['instagram', new InstagramPlatform()],
  ['linkedin', new LinkedInPlatform()],
]);

export function getPlatform(name: string): SocialPlatform {
  const platform = platforms.get(name.toLowerCase());
  if (!platform) {
    throw new InvalidPlatformError(name);
  }
  return platform;
}

export function listPlatforms(): readonly string[] {
  return [...platforms.keys()];
}

export type { SocialPlatform, SessionStatus } from '../../shared/model/models.js';
