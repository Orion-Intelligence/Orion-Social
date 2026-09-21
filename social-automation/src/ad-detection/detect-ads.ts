#!/usr/bin/env node

import { XAdDetector } from './platforms/x.js';
import { InstagramAdDetector } from './platforms/instagram.js';
import { FacebookAdDetector } from './platforms/facebook.js';
import { RedditAdDetector } from './platforms/reddit.js';
import { PinterestAdDetector } from './platforms/pinterest.js';
import { YouTubeAdDetector } from './platforms/youtube.js';
import { TikTokAdDetector } from './platforms/tiktok.js';
import { ThreadsAdDetector } from './platforms/threads.js';
import { QuoraAdDetector } from './platforms/quora.js';
import { OkRuAdDetector } from './platforms/okru.js';
import { PatreonAdDetector } from './platforms/patreon.js';
import { HashnodeAdDetector } from './platforms/hashnode.js';
import { BehanceAdDetector } from './platforms/behance.js';
import { LinkedInAdDetector } from './platforms/linkedin.js';
import { MeWeAdDetector } from './platforms/mewe.js';
import { parseResultFileArg, writeResult } from '../shared/result-writer.js';
import type { AdDetectionResult } from './model/models.js';

interface DetectArgs {
  platform: string;
  sessionFile?: string;
  resultFile?: string;
}

function parseArgs(argv: string[]): DetectArgs {
  const args = argv.slice(2);
  let platform = '';
  let sessionFile: string | undefined;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i] ?? '';
    const next = args[i + 1];

    switch (arg) {
      case '--platform':
        if (!next) {
          process.exit(1);
        }
        platform = next;
        i++;
        break;
      case '--session-file':
        if (!next) {
          process.exit(1);
        }
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

  const resultFile = parseResultFileArg(argv);
  return { platform: platform.toLowerCase(), sessionFile, resultFile };
}

async function main() {
  const { platform, sessionFile, resultFile } = parseArgs(process.argv);
  (global as any).RESULT_FILE = resultFile;

  let result: AdDetectionResult;
  if (platform === 'x' || platform === 'twitter') {
    result = await new XAdDetector(sessionFile).run();
  } else if (platform === 'instagram' || platform === 'ig') {
    result = await new InstagramAdDetector(sessionFile).run();
  } else if (platform === 'facebook') {
    result = await new FacebookAdDetector(sessionFile).run();
  } else if (platform === 'reddit') {
    result = await new RedditAdDetector(sessionFile).run();
  } else if (platform === 'pinterest') {
    result = await new PinterestAdDetector(sessionFile).run();
  } else if (platform === 'youtube') {
    result = await new YouTubeAdDetector(sessionFile).run();
  } else if (platform === 'tiktok') {
    result = await new TikTokAdDetector(sessionFile).run();
  } else if (platform === 'threads') {
    result = await new ThreadsAdDetector(sessionFile).run();
  } else if (platform === 'quora') {
    result = await new QuoraAdDetector(sessionFile).run();
  } else if (platform === 'okru') {
    result = await new OkRuAdDetector(sessionFile).run();
  } else if (platform === 'patreon') {
    result = await new PatreonAdDetector(sessionFile).run();
  } else if (platform === 'hashnode') {
    result = await new HashnodeAdDetector(sessionFile).run();
  } else if (platform === 'behance') {
    result = await new BehanceAdDetector(sessionFile).run();
  } else if (platform === 'linkedin') {
    result = await new LinkedInAdDetector(sessionFile).run();
  } else if (platform === 'mewe') {
    result = await new MeWeAdDetector(sessionFile).run();
  } else {
    console.error(`Unsupported platform for ad detection: ${platform}`);
    process.exit(1);
  }

  writeResult(resultFile, result);
}

main().catch(() => {});
