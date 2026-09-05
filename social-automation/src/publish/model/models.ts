import type { Page } from 'playwright';

import type { AutomationResult, SocialPlatformName } from '../../shared/model/models.js';

export interface PublishPost {
  readonly text: string;
  readonly images?: readonly string[];
  readonly videos?: readonly string[];
  readonly platforms: readonly SocialPlatformName[];
}

export interface PublishResult {
  readonly platform: SocialPlatformName;
  readonly success: boolean;
  readonly postUrl?: string;
  readonly error?: string;
  readonly errorCode?: string;
}

export type PublishStatus = 'pending' | 'publishing' | 'success' | 'failed' | 'verification_failed';

export interface PublishOperation {
  readonly operationId: string;
  readonly platform: SocialPlatformName;
  readonly startedAt: Date;
  status: PublishStatus;
  error?: string;
  postUrl?: string;
}

export interface SocialPlatformAdapter {
  readonly platform: SocialPlatformName;
  readonly displayName: string;

  readonly supportedImageExtensions: readonly string[];
  readonly supportedVideoExtensions: readonly string[];
  readonly maxImages: number;


  openComposer(page: Page): Promise<void>;

  createPost(page: Page, post: PublishPost): Promise<void>;

  publishPost(page: Page): Promise<void>;

  verifyPublished(page: Page): Promise<{
    success: boolean;
    postUrl?: string;
  }>;
}

export interface PublishOptions {
  readonly dryRun?: boolean;
  readonly sessionFile?: string;
}

export interface PostResult extends AutomationResult {
  post_url: string;
}
