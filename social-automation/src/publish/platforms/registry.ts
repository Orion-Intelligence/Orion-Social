import type { SocialPlatformAdapter } from '../model/models.js';
import type { SocialPlatformName } from '../../shared/model/models.js';
import { FacebookAdapter } from './facebook.js';
import { XAdapter } from './x.js';
import { InstagramAdapter } from './instagram.js';
import { LinkedInAdapter } from './linkedin.js';
import { ThreadsAdapter } from './threads.js';
import { RedditAdapter } from './reddit.js';
import { PinterestAdapter } from './pinterest.js';
import { YouTubeAdapter } from './youtube.js';
import { TikTokAdapter } from './tiktok.js';
import { QuoraAdapter } from './quora.js';
import { OkRuAdapter } from './okru.js';
import { PatreonAdapter } from './patreon.js';
import { HashnodeAdapter } from './hashnode.js';
import { BehanceAdapter } from './behance.js';
import { MeWeAdapter } from './mewe.js';
import { InvalidPlatformError } from '../../shared/errors.js';

const entries: [SocialPlatformName, SocialPlatformAdapter][] = [
  ['facebook', new FacebookAdapter()],
  ['x', new XAdapter()],
  ['instagram', new InstagramAdapter()],
  ['linkedin', new LinkedInAdapter()],
  ['threads', new ThreadsAdapter()],
  ['reddit', new RedditAdapter()],
  ['pinterest', new PinterestAdapter()],
  ['youtube', new YouTubeAdapter()],
  ['tiktok', new TikTokAdapter()],
  ['quora', new QuoraAdapter()],
  ['okru', new OkRuAdapter()],
  ['patreon', new PatreonAdapter()],
  ['hashnode', new HashnodeAdapter()],
  ['behance', new BehanceAdapter()],
  ['mewe', new MeWeAdapter()],
];
const adapters: ReadonlyMap<SocialPlatformName, SocialPlatformAdapter> = new Map(entries);

export function getAdapter(platform: string): SocialPlatformAdapter {
  const adapter = adapters.get(platform.toLowerCase() as SocialPlatformName);
  if (!adapter) {
    throw new InvalidPlatformError(platform);
  }
  return adapter;
}
