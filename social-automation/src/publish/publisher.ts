import crypto from 'node:crypto';
import type { BrowserContext } from 'playwright';


import { SocialAutomationError } from '../shared/errors.js';
import { getSocialContext } from '../session/session-manager.js';
import { trackContext, untrackContext } from '../session/shutdown.js';
import { getAdapter } from './platforms/registry.js';
import { validateImages } from './media.js';
import { VerificationError } from '../shared/errors.js';
import type {
  PublishPost,
  PublishResult,
  PublishOperation,
  PublishOptions,
} from './model/models.js';
import type { SocialPlatformName } from '../shared/model/models.js';

export class SocialPublisher {
  
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
      
      const adapter = getAdapter(platformName);

      if (post.images && post.images.length > 0) {
        validateImages(
          post.images,
          adapter.supportedImageExtensions,
          adapter.maxImages,
        );
      }



      console.log(`[Post] Starting publish on ${platformName}`);
      context = await getSocialContext(platformName, userId, options.sessionFile);
      trackContext(context);

      const page = context.pages()[0] ?? await context.newPage();

      console.log(`[Post] Opening composer`);
      operation.status = 'publishing';
      await adapter.openComposer(page);

      console.log(`[Post] Writing post content${post.images?.length ? ` with ${post.images.length} image(s)` : ''}`);
      await adapter.createPost(page, post);

      if (options.dryRun) {
        console.log(`[Post] Dry run, not publishing`);
        operation.status = 'success';
        return {
          platform: platformName,
          success: true,
          postUrl: undefined,
          error: undefined,
        };
      }


      console.log(`[Post] Publishing`);
      await adapter.publishPost(page);

      console.log(`[Post] Verifying the post was published`);
      const verification = await adapter.verifyPublished(page);

      if (verification.success) {
        operation.status = 'success';
        operation.postUrl = verification.postUrl;
        console.log(`[Post] Published: ${verification.postUrl ?? '(no URL returned)'}`);
      } else {
        console.log(`[Post] Could not confirm the post was published`);
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

      console.log(`[Post] Failed (${code}): ${message}`);

      return {
        platform: platformName,
        success: false,
        error: message,
        errorCode: code,
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

    }
  }
}
