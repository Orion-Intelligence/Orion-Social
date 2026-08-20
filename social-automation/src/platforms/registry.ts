import type { SocialPlatform } from './types.js';
import { FacebookPlatform } from './facebook.js';
import { XPlatform } from './x.js';
import { InstagramPlatform } from './instagram.js';
import { LinkedInPlatform } from './linkedin.js';
import { InvalidPlatformError } from '../errors.js';

/** Immutable map of platform identifier → platform instance. */
const platforms: ReadonlyMap<string, SocialPlatform> = new Map<string, SocialPlatform>([
  ['facebook', new FacebookPlatform()],
  ['x', new XPlatform()],
  ['instagram', new InstagramPlatform()],
  ['linkedin', new LinkedInPlatform()],
]);

/**
 * Retrieve a registered platform by its lowercase identifier.
 * @throws {InvalidPlatformError} if the identifier is not registered.
 */
export function getPlatform(name: string): SocialPlatform {
  const platform = platforms.get(name.toLowerCase());
  if (!platform) {
    throw new InvalidPlatformError(name);
  }
  return platform;
}

/** Return the list of all registered platform identifiers. */
export function listPlatforms(): readonly string[] {
  return [...platforms.keys()];
}

// Re-export types for convenience.
export type { SocialPlatform, SocialPost, PostResult, SessionStatus } from './types.js';
