#!/usr/bin/env node
/**
 * CLI: publish a post to one or more social platforms.
 *
 * Usage:
 *   npm run social:post -- --platform facebook,x --text "Hello from Orion"
 *   npm run social:post -- --platform facebook --text-file post.txt
 *   npm run social:post -- --platform facebook --text "Update" --image ./photo.jpg
 *   npm run social:post -- --platform facebook,x --text "Test" --dry-run
 */

import fs from 'node:fs';
import path from 'node:path';
import { SocialPublisher } from '../publish/publisher.js';
import { SocialAutomationError } from '../errors.js';
import { logger } from '../logger.js';
import { isPlatformName, PLATFORM_NAMES } from '../publish/types.js';
import type { SocialPlatformName, PublishPost } from '../publish/types.js';

interface PostArgs {
  platforms: SocialPlatformName[];
  text: string;
  images: string[];
  dryRun: boolean;
}

function parseArgs(argv: string[]): PostArgs {
  const args = argv.slice(2); // Drop node + script path.

  let rawPlatform = '';
  let text = '';
  let textFile = '';
  const images: string[] = [];
  let dryRun = false;

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

      default:
        // Skip unknown args gracefully (tsx may inject some).
        break;
    }
  }

  // Resolve text.
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

  // Parse and validate platforms.
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

  return { platforms, text, images, dryRun };
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
  const { platforms, text, images, dryRun } = parseArgs(process.argv);

  if (dryRun) {
    logger.info('DRY RUN mode – posts will NOT be published');
  }

  const post: PublishPost = {
    text,
    images: images.length > 0 ? images : undefined,
    platforms,
  };

  const publisher = new SocialPublisher();

  try {
    const results = await publisher.publish(post, { dryRun });

    // Print results.
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
        // Extract actionable hint from the error.
        if (result.error.includes('AUTHENTICATION')) {
          console.log(`   Action: Provide a new session file for ${result.platform} from Orion Intelligence.`);
        }
        hasFailure = true;
      }
      console.log('');
    }

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
    process.exit(1);
  }
}

main();
