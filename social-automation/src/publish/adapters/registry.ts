import type { SocialPlatformAdapter, SocialPlatformName } from '../types.js';
import { FacebookAdapter } from './facebook.js';
import { XAdapter } from './x.js';
import { InstagramAdapter } from './instagram.js';
import { LinkedInAdapter } from './linkedin.js';
import { InvalidPlatformError } from '../../errors.js';

/** Immutable map of platform name → publishing adapter. */
const entries: [SocialPlatformName, SocialPlatformAdapter][] = [
  ['facebook', new FacebookAdapter()],
  ['x', new XAdapter()],
  ['instagram', new InstagramAdapter()],
  ['linkedin', new LinkedInAdapter()],
];
const adapters: ReadonlyMap<SocialPlatformName, SocialPlatformAdapter> = new Map(entries);

/**
 * Retrieve the publishing adapter for a platform.
 * @throws {InvalidPlatformError} if the platform is not registered.
 */
export function getAdapter(platform: string): SocialPlatformAdapter {
  const adapter = adapters.get(platform.toLowerCase() as SocialPlatformName);
  if (!adapter) {
    throw new InvalidPlatformError(platform);
  }
  return adapter;
}

/** Return all registered adapter instances. */
export function getAllAdapters(): readonly SocialPlatformAdapter[] {
  return [...adapters.values()];
}
