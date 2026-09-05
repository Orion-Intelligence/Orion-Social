import type { SocialPlatformAdapter } from '../model/models.js';
import type { SocialPlatformName } from '../../shared/model/models.js';
import { FacebookAdapter } from './facebook.js';
import { XAdapter } from './x.js';
import { InstagramAdapter } from './instagram.js';
import { LinkedInAdapter } from './linkedin.js';
import { InvalidPlatformError } from '../../shared/errors.js';

const entries: [SocialPlatformName, SocialPlatformAdapter][] = [
  ['facebook', new FacebookAdapter()],
  ['x', new XAdapter()],
  ['instagram', new InstagramAdapter()],
  ['linkedin', new LinkedInAdapter()],
];
const adapters: ReadonlyMap<SocialPlatformName, SocialPlatformAdapter> = new Map(entries);

export function getAdapter(platform: string): SocialPlatformAdapter {
  const adapter = adapters.get(platform.toLowerCase() as SocialPlatformName);
  if (!adapter) {
    throw new InvalidPlatformError(platform);
  }
  return adapter;
}

export function getAllAdapters(): readonly SocialPlatformAdapter[] {
  return [...adapters.values()];
}
