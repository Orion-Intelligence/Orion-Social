import type { Page } from 'playwright';

export interface SocialPost {
  readonly text?: string;
  readonly mediaUrls?: readonly string[];
  readonly mediaFiles?: readonly string[];
  readonly link?: string;
  readonly title?: string;
}

export interface PostResult {
  readonly success: boolean;
  readonly postId?: string;
  readonly postUrl?: string;
  readonly error?: string;
}

export interface SessionStatus {
  readonly platform: string;
  readonly authenticated: boolean;
  readonly profileConfigured: boolean;
  readonly profilePath: string;
}

export interface SocialPlatform {
  
  readonly name: string;

  readonly displayName: string;

  readonly loginUrl: string;

  isAuthenticated(page: Page, navigate?: boolean): Promise<boolean>;

  createPost?(page: Page, post: SocialPost): Promise<PostResult>;
}

export type SocialPlatformName = 'facebook' | 'x' | 'instagram' | 'linkedin';

export const PLATFORM_NAMES: readonly SocialPlatformName[] = Object.freeze([
  'facebook', 'x', 'instagram', 'linkedin',
] as const);

export function isPlatformName(value: string): value is SocialPlatformName {
  return (PLATFORM_NAMES as readonly string[]).includes(value.toLowerCase());
}

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
