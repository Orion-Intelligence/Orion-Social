import type { Page } from 'playwright';

// ---------------------------------------------------------------------------
// Platform name union
// ---------------------------------------------------------------------------

/** All supported social platform identifiers. */
export type SocialPlatformName = 'facebook' | 'x' | 'instagram' | 'linkedin';

export const PLATFORM_NAMES: readonly SocialPlatformName[] = Object.freeze([
  'facebook', 'x', 'instagram', 'linkedin',
] as const);

/** Type guard for SocialPlatformName. */
export function isPlatformName(value: string): value is SocialPlatformName {
  return (PLATFORM_NAMES as readonly string[]).includes(value.toLowerCase());
}

// ---------------------------------------------------------------------------
// Post models
// ---------------------------------------------------------------------------

/** Input model for a social-media post to be published across platforms. */
export interface PublishPost {
  readonly text: string;
  readonly images?: readonly string[];
  readonly videos?: readonly string[];
  readonly platforms: readonly SocialPlatformName[];
}

/** Per-platform result of a publish attempt. Never contains credentials. */
export interface PublishResult {
  readonly platform: SocialPlatformName;
  readonly success: boolean;
  readonly postUrl?: string;
  readonly error?: string;
}

/** Publish-operation status for idempotency tracking. */
export type PublishStatus = 'pending' | 'publishing' | 'success' | 'failed' | 'verification_failed';

/** Internal tracking record for a single platform publish operation. */
export interface PublishOperation {
  readonly operationId: string;
  readonly platform: SocialPlatformName;
  readonly startedAt: Date;
  status: PublishStatus;
  error?: string;
  postUrl?: string;
}

// ---------------------------------------------------------------------------
// Platform adapter interface
// ---------------------------------------------------------------------------

/**
 * Contract for platform-specific publishing adapters.
 *
 * Each adapter encapsulates the full posting workflow for a single platform.
 * Platform-specific selectors and DOM interactions are isolated here so that
 * the SocialPublisher orchestrator remains platform-agnostic.
 */
export interface SocialPlatformAdapter {
  readonly platform: SocialPlatformName;
  readonly displayName: string;

  /** Supported media extensions for this platform. */
  readonly supportedImageExtensions: readonly string[];
  readonly supportedVideoExtensions: readonly string[];
  readonly maxImages: number;

  /** Check whether the current session is authenticated. */
  isAuthenticated(page: Page): Promise<boolean>;

  /** Navigate to and open the post composer. */
  openComposer(page: Page): Promise<void>;

  /** Fill in the post content (text, media). */
  createPost(page: Page, post: PublishPost): Promise<void>;

  /** Click the publish/post button. */
  publishPost(page: Page): Promise<void>;

  /**
   * Verify that the post was actually published.
   * Returns success status and optionally the resulting post URL.
   */
  verifyPublished(page: Page): Promise<{
    success: boolean;
    postUrl?: string;
  }>;
}

/** Options controlling the publish flow. */
export interface PublishOptions {
  readonly dryRun?: boolean;
}
