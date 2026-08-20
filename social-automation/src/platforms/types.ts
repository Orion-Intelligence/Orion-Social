import type { Page } from 'playwright';

/**
 * Payload for creating a social-media post.
 * Fields are optional since different platforms support different features.
 */
export interface SocialPost {
  readonly text?: string;
  readonly mediaUrls?: readonly string[];
  readonly mediaFiles?: readonly string[];
  readonly link?: string;
  readonly title?: string;
}

/** Outcome of a post-creation attempt. */
export interface PostResult {
  readonly success: boolean;
  readonly postId?: string;
  readonly postUrl?: string;
  readonly error?: string;
}

/** Safe session-status information (never includes credentials). */
export interface SessionStatus {
  readonly platform: string;
  readonly authenticated: boolean;
  readonly profileConfigured: boolean;
  readonly profilePath: string;
}

/**
 * Contract that every social-platform adapter must implement.
 *
 * To add a new platform:
 *   1. Create a file in src/platforms/ implementing this interface.
 *   2. Register it in src/platforms/registry.ts.
 */
export interface SocialPlatform {
  /** Machine-readable lowercase identifier (e.g. "facebook", "x"). */
  readonly name: string;

  /** Human-readable display name (e.g. "Facebook", "X (Twitter)"). */
  readonly displayName: string;

  /** URL to navigate to for the manual login flow. */
  readonly loginUrl: string;

  /**
   * Determine whether the current page state indicates a valid
   * authenticated session.
   *
   * Implementations should use stable, platform-specific signals
   * (e.g. presence of user-avatar elements, profile links, specific
   * cookies) rather than simply checking if a homepage loaded.
   */
  isAuthenticated(page: Page, navigate?: boolean): Promise<boolean>;

  /**
   * Optional: create and publish a post.
   * Only implement when the posting workflow is ready for a platform.
   */
  createPost?(page: Page, post: SocialPost): Promise<PostResult>;
}
