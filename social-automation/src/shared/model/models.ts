import type { Page } from 'playwright';

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
}

export type SocialPlatformName = 'facebook' | 'x' | 'instagram' | 'linkedin';

export const PLATFORM_NAMES: readonly SocialPlatformName[] = Object.freeze([
  'facebook', 'x', 'instagram', 'linkedin',
] as const);

export function isPlatformName(value: string): value is SocialPlatformName {
  return (PLATFORM_NAMES as readonly string[]).includes(value.toLowerCase());
}

export interface AutomationResult {
  error: boolean;
  error_reason: string;
  session_expired: boolean;
}
