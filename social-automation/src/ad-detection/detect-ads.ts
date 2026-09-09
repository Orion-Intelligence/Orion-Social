#!/usr/bin/env node

import { detectAds as detectXAds } from './platforms/x.js';
import { detectAds as detectIgAds } from './platforms/instagram.js';
import { parseResultFileArg } from '../shared/result-writer.js';

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

  if (platform === 'x' || platform === 'twitter') {
    await detectXAds(sessionFile, resultFile);
  } else if (platform === 'instagram' || platform === 'ig') {
    await detectIgAds(sessionFile, resultFile);
  } else {
    console.error(`Unsupported platform for ad detection: ${platform}`);
    process.exit(1);
  }
}

main().catch(() => {});
