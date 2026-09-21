import type { SocialPlatform } from '../../shared/model/models.js';
import { FacebookPlatform } from './facebook.js';
import { XPlatform } from './x.js';
import { InstagramPlatform } from './instagram.js';
import { LinkedInPlatform } from './linkedin.js';
import { ThreadsPlatform } from './threads.js';
import { RedditPlatform } from './reddit.js';
import { PinterestPlatform } from './pinterest.js';
import { YouTubePlatform } from './youtube.js';
import { TikTokPlatform } from './tiktok.js';
import { QuoraPlatform } from './quora.js';
import { OkRuPlatform } from './okru.js';
import { PatreonPlatform } from './patreon.js';
import { HashnodePlatform } from './hashnode.js';
import { BehancePlatform } from './behance.js';
import { MeWePlatform } from './mewe.js';
import { InvalidPlatformError } from '../../shared/errors.js';

const platforms: ReadonlyMap<string, SocialPlatform> = new Map<string, SocialPlatform>([
  ['facebook', new FacebookPlatform()],
  ['x', new XPlatform()],
  ['instagram', new InstagramPlatform()],
  ['linkedin', new LinkedInPlatform()],
  ['threads', new ThreadsPlatform()],
  ['reddit', new RedditPlatform()],
  ['pinterest', new PinterestPlatform()],
  ['youtube', new YouTubePlatform()],
  ['tiktok', new TikTokPlatform()],
  ['quora', new QuoraPlatform()],
  ['okru', new OkRuPlatform()],
  ['patreon', new PatreonPlatform()],
  ['hashnode', new HashnodePlatform()],
  ['behance', new BehancePlatform()],
  ['mewe', new MeWePlatform()],
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
