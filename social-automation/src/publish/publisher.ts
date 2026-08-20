import crypto from 'node:crypto';
import type { BrowserContext } from 'playwright';

import { logger } from '../logger.js';
import { SocialAutomationError } from '../errors.js';
import { getSocialContext } from '../session/manager.js';
import { trackContext, untrackContext } from '../session/shutdown.js';
import { getAdapter } from './adapters/registry.js';
import { validateImages } from './media.js';
import { AuthenticationError, VerificationError } from './errors.js';
import type {
  PublishPost,
  PublishResult,
  PublishOperation,
  PublishOptions,
  SocialPlatformName,
} from './types.js';

/**
 * Orchestrate publishing a single post across one or more social platforms.
 *
 * The publisher:
 *   - Validates the post and media upfront.
 *   - Iterates over requested platforms independently (one failure does not abort others).
 *   - Tracks each operation for idempotency.
 *   - Never exposes credentials in results.
 *   - Supports dry-run mode.
 */
export class SocialPublisher {
  /**
   * Publish a post to all requested platforms.
   * Returns one result per platform; failures do not abort remaining platforms.
   */
  async publish(
    post: PublishPost,
    options: PublishOptions = {},
    userId: string = 'default'
  ): Promise<readonly PublishResult[]> {
    const results: PublishResult[] = [];

    for (const platformName of post.platforms) {
      const result = await this.publishToSinglePlatform(
        platformName,
        post,
        options,
        userId
      );
      results.push(result);
    }

    return results;
  }

  private async publishToSinglePlatform(
    platformName: SocialPlatformName,
    post: PublishPost,
    options: PublishOptions,
    userId: string
  ): Promise<PublishResult> {
    const operation = this.createOperation(platformName);
    let context: BrowserContext | null = null;

    try {
      // 1. Get the adapter.
      const adapter = getAdapter(platformName);

      // 2. Validate media upfront if provided.
      if (post.images && post.images.length > 0) {
        validateImages(
          post.images,
          adapter.supportedImageExtensions,
          adapter.maxImages,
        );
      }

      logger.info(`[${platformName}] Opening persistent profile (User: ${userId})`);

      // 3. Launch ephemeral context using session JSON.
      context = await getSocialContext(platformName, userId);
      trackContext(context);

      const page = context.pages()[0] ?? await context.newPage();

      // 4. Verify authentication.
      logger.info(`[${platformName}] Verifying authentication`);
      const authenticated = await adapter.isAuthenticated(page);
      if (!authenticated) {
        throw new AuthenticationError(platformName);
      }
      logger.info(`[${platformName}] Authenticated ✔`);

      // 5. Open the composer.
      logger.info(`[${platformName}] Opening composer`);
      operation.status = 'publishing';
      await adapter.openComposer(page);

      // 6. Create the post content.
      logger.info(`[${platformName}] Creating post content`);
      await adapter.createPost(page, post);

      // 7. Dry-run check: stop before actually publishing.
      if (options.dryRun) {
        logger.info(`[${platformName}] DRY RUN – skipping publish`);
        operation.status = 'success';
        return {
          platform: platformName,
          success: true,
          postUrl: undefined,
          error: undefined,
        };
      }

      // 8. Publish.
      logger.info(`[${platformName}] Publishing…`);
      await adapter.publishPost(page);

      // 9. Verify publication.
      logger.info(`[${platformName}] Verifying publication`);
      const verification = await adapter.verifyPublished(page);

      if (verification.success) {
        operation.status = 'success';
        operation.postUrl = verification.postUrl;
        logger.info(`[${platformName}] Published successfully`, {
          postUrl: verification.postUrl ?? '(URL not available)',
        });
      } else {
        // Uncertain state – do NOT retry to avoid duplicates.
        operation.status = 'verification_failed';
        throw new VerificationError(
          platformName,
          'Could not confirm the post was published',
        );
      }

      return {
        platform: platformName,
        success: true,
        postUrl: verification.postUrl,
      };
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : String(err);
      const code = err instanceof SocialAutomationError
        ? (err as SocialAutomationError).code
        : 'UNKNOWN';

      operation.status = 'failed';
      operation.error = message;

      logger.error(`[${platformName}] ${message}`, { code });

      return {
        platform: platformName,
        success: false,
        error: message,
      };
    } finally {
      if (context) {
        untrackContext(context);
        await this.safeClose(context);
      }
    }
  }

  private createOperation(platform: SocialPlatformName): PublishOperation {
    return {
      operationId: crypto.randomUUID(),
      platform,
      startedAt: new Date(),
      status: 'pending',
    };
  }

  private async safeClose(context: BrowserContext): Promise<void> {
    try {
      await context.close();
    } catch (err: unknown) {
      logger.warn('Error closing browser context', {
        error: err instanceof Error ? err.message : String(err),
      });
    }
  }
}
