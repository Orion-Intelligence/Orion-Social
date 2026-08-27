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
