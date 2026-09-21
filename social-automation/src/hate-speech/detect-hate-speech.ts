#!/usr/bin/env node

import { XHateSpeechMonitor } from './platforms/x.js';
import { InstagramHateSpeechMonitor } from './platforms/instagram.js';
import { FacebookHateSpeechMonitor } from './platforms/facebook.js';
import { RedditHateSpeechMonitor } from './platforms/reddit.js';
import { PinterestHateSpeechMonitor } from './platforms/pinterest.js';
import { YouTubeHateSpeechMonitor } from './platforms/youtube.js';
import { TikTokHateSpeechMonitor } from './platforms/tiktok.js';
import { ThreadsHateSpeechMonitor } from './platforms/threads.js';
import { QuoraHateSpeechMonitor } from './platforms/quora.js';
import { OkRuHateSpeechMonitor } from './platforms/okru.js';
import { PatreonHateSpeechMonitor } from './platforms/patreon.js';
import { HashnodeHateSpeechMonitor } from './platforms/hashnode.js';
import { BehanceHateSpeechMonitor } from './platforms/behance.js';
import { LinkedInHateSpeechMonitor } from './platforms/linkedin.js';
import { MeWeHateSpeechMonitor } from './platforms/mewe.js';
import { parseResultFileArg, writeResult } from '../shared/result-writer.js';
import type { HateSpeechMonitorResult } from './model/models.js';

interface DetectArgs {
  platform: string;
  profileUrl: string;
  postCount: number;
  sessionFile?: string;
  resultFile?: string;
}

function parseArgs(argv: string[]): DetectArgs {
  const args = argv.slice(2);
  let platform = '';
  let profileUrl = '';
  let postCount = 50;
  let sessionFile: string | undefined;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i] ?? '';
    const next = args[i + 1];

    switch (arg) {
      case '--platform':
        platform = next;
        i++;
        break;
      case '--profile-url':
        profileUrl = next;
        i++;
        break;
      case '--post-count':
        postCount = parseInt(next, 10) || 50;
        i++;
        break;
      case '--session-file':
        sessionFile = next;
        i++;
        break;
      case '--result-file':
        i++;
        break;
      default:
        break;
    }
  }

  if (!platform) {
    console.error('Platform is required (--platform)');
    process.exit(1);
  }
  if (!profileUrl) {
    console.error('Profile URL is required (--profile-url)');
    process.exit(1);
  }

  const resultFile = parseResultFileArg(argv);
  return { platform: platform.toLowerCase(), profileUrl, postCount, sessionFile, resultFile };
}

async function main() {
  const { platform, profileUrl, postCount, sessionFile, resultFile } = parseArgs(process.argv);
  console.log(`[Main] Running detect-hate-speech on ${platform} for ${profileUrl} (count: ${postCount})`);
  (global as any).RESULT_FILE = resultFile;

  let result: HateSpeechMonitorResult;
  if (platform === 'x' || platform === 'twitter') {
    result = await new XHateSpeechMonitor(sessionFile, profileUrl, postCount).run();
  } else if (platform === 'instagram' || platform === 'ig') {
    result = await new InstagramHateSpeechMonitor(sessionFile, profileUrl, postCount).run();
  } else if (platform === 'facebook') {
    result = await new FacebookHateSpeechMonitor(sessionFile, profileUrl, postCount).run();
  } else if (platform === 'reddit') {
    result = await new RedditHateSpeechMonitor(sessionFile, profileUrl, postCount).run();
  } else if (platform === 'pinterest') {
    result = await new PinterestHateSpeechMonitor(sessionFile, profileUrl, postCount).run();
  } else if (platform === 'youtube') {
    result = await new YouTubeHateSpeechMonitor(sessionFile, profileUrl, postCount).run();
  } else if (platform === 'tiktok') {
    result = await new TikTokHateSpeechMonitor(sessionFile, profileUrl, postCount).run();
  } else if (platform === 'threads') {
    result = await new ThreadsHateSpeechMonitor(sessionFile, profileUrl, postCount).run();
  } else if (platform === 'quora') {
    result = await new QuoraHateSpeechMonitor(sessionFile, profileUrl, postCount).run();
  } else if (platform === 'okru') {
    result = await new OkRuHateSpeechMonitor(sessionFile, profileUrl, postCount).run();
  } else if (platform === 'patreon') {
    result = await new PatreonHateSpeechMonitor(sessionFile, profileUrl, postCount).run();
  } else if (platform === 'hashnode') {
    result = await new HashnodeHateSpeechMonitor(sessionFile, profileUrl, postCount).run();
  } else if (platform === 'behance') {
    result = await new BehanceHateSpeechMonitor(sessionFile, profileUrl, postCount).run();
  } else if (platform === 'linkedin') {
    result = await new LinkedInHateSpeechMonitor(sessionFile, profileUrl, postCount).run();
  } else if (platform === 'mewe') {
    result = await new MeWeHateSpeechMonitor(sessionFile, profileUrl, postCount).run();
  } else {
    console.error(`Unsupported platform for hate speech monitoring: ${platform}`);
    process.exit(1);
  }

  writeResult(resultFile, result);
}

main().catch((err) => {
  console.error('[Fatal Error] in detect-hate-speech:', err);
  process.exit(1);
});
