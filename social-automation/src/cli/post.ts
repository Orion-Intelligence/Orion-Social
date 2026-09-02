#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { SocialPublisher } from '../publish/publisher.js';
import { SocialAutomationError } from '../errors.js';
import { logger } from '../logger.js';
import { isPlatformName, PLATFORM_NAMES } from '../publish/types.js';
import type { SocialPlatformName, PublishPost } from '../publish/types.js';
import { errorReason, isSessionExpired, isSessionExpiredCode, parseResultFileArg, writeResult } from '../result.js';
import type { PostResult } from '../result.js';

interface PostArgs {
  platforms: SocialPlatformName[];
  text: string;
  images: string[];
  dryRun: boolean;
  sessionFile?: string;
}

function parseArgs(argv: string[]): PostArgs {
  const args = argv.slice(2); 

  let rawPlatform = '';
  let text = '';
  let textFile = '';
  const images: string[] = [];
  let dryRun = false;
  let sessionFile: string | undefined;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i] ?? '';
    const next = args[i + 1];

    switch (arg) {
      case '--platform':
        if (!next) {
          exitUsage('Missing value for --platform');
        }
        rawPlatform = next;
        i++;
        break;

      case '--text':
        if (!next) {
          exitUsage('Missing value for --text');
        }
        text = next;
        i++;
        break;

      case '--text-file':
        if (!next) {
          exitUsage('Missing value for --text-file');
        }
        textFile = next;
        i++;
        break;

      case '--image':
        if (!next) {
          exitUsage('Missing value for --image');
        }
        images.push(next);
        i++;
        break;

      case '--dry-run':
        dryRun = true;
        break;

      case '--session-file':
        if (!next) {
          exitUsage('Missing value for --session-file');
        }
        sessionFile = next;
        i++;
        break;

      case '--result-file':
        if (!next) {
          exitUsage('Missing value for --result-file');
        }
        i++;
        break;

      default:
        
        break;
    }
  }

  if (textFile) {
    const filePath = path.resolve(textFile);
    if (!fs.existsSync(filePath)) {
      console.error(`Error: text file not found: ${filePath}`);
      process.exit(1);
    }
    text = fs.readFileSync(filePath, 'utf-8').trim();
  }

  if (!text) {
    exitUsage('Post text is required (--text or --text-file)');
  }

  if (!rawPlatform) {
    exitUsage('At least one platform is required (--platform)');
  }

  const platformNames = rawPlatform.split(',').map((p) => p.trim().toLowerCase());
  const platforms: SocialPlatformName[] = [];
  for (const name of platformNames) {
    if (!isPlatformName(name)) {
      console.error(
        `Unknown platform: "${name}". Available: ${PLATFORM_NAMES.join(', ')}`,
      );
      process.exit(1);
    }
    platforms.push(name);
  }

  return { platforms, text, images, dryRun, sessionFile };
}

function exitUsage(error: string): never {
  console.error(`Error: ${error}\n`);
  console.error(
    'Usage:\n' +
    '  npm run social:post -- --platform facebook,x --text "Hello"\n' +
    '  npm run social:post -- --platform facebook --text-file post.txt\n' +
    '  npm run social:post -- --platform facebook --text "Hi" --image ./photo.jpg\n' +
    '  npm run social:post -- --platform facebook,x --text "Test" --dry-run\n' +
    `\nAvailable platforms: ${PLATFORM_NAMES.join(', ')}`,
  );
  process.exit(1);
}

async function main(): Promise<void> {
  const { platforms, text, images, dryRun, sessionFile } = parseArgs(process.argv);

  if (dryRun) {
    logger.info('DRY RUN mode – posts will NOT be published');
  }

  const post: PublishPost = {
    text,
    images: images.length > 0 ? images : undefined,
    platforms,
  };

  const publisher = new SocialPublisher();

  const resultFile = parseResultFileArg(process.argv);
  const postResult: PostResult = {
    post_url: '',
    error: false,
    error_reason: '',
    session_expired: false,
  };

  try {
    const results = await publisher.publish(post, { dryRun, sessionFile });

    const primary = results.find((item) => item.platform === platforms[0]) ?? results[0];
    if (primary) {
      postResult.post_url = primary.postUrl ?? '';
      postResult.error = !primary.success;
      postResult.error_reason = primary.error ?? '';
      postResult.session_expired = isSessionExpiredCode(primary.errorCode);
    }

    console.log('\n═══════════════════════════════════');
    console.log(dryRun ? ' DRY RUN RESULTS' : ' PUBLISH RESULTS');
    console.log('═══════════════════════════════════\n');

    let hasFailure = false;

    for (const result of results) {
      const icon = result.success ? '✔' : '✘';
      const status = result.success ? 'SUCCESS' : 'FAILED';

      console.log(`${icon}  ${result.platform.toUpperCase()}: ${status}`);

      if (result.postUrl) {
        console.log(`   Post URL: ${result.postUrl}`);
      }
      if (result.error) {
        console.log(`   Reason: ${result.error}`);
        
        if (result.error.includes('AUTHENTICATION')) {
          console.log(`   Action: Provide a new session file for ${result.platform} from Orion Intelligence.`);
        }
        hasFailure = true;
      }
      console.log('');
    }

    writeResult(resultFile, postResult);

    if (hasFailure) {
      process.exit(1);
    }
  } catch (err: unknown) {
    if (err instanceof SocialAutomationError) {
      logger.error(err.message, { code: err.code });
    } else {
      logger.error('Unexpected error during publishing', {
        error: err instanceof Error ? err.message : String(err),
      });
    }
    postResult.error = true;
    postResult.error_reason = errorReason(err);
    postResult.session_expired = isSessionExpired(err);
    writeResult(resultFile, postResult);
    process.exit(1);
  }
}

main();
