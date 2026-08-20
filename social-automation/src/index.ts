/**
 * @module @orion/social-automation
 *
 * Public API surface for the Orion social-media session manager and publisher.
 *
 * This module allows Orion to:
 *   1. Perform a manual one-time login to social platforms.
 *   2. Persist browser sessions locally via Playwright persistent contexts.
 *   3. Reuse those sessions for subsequent automated actions.
 *   4. Publish posts to multiple social platforms simultaneously.
 */

// Session management
export {
  getSocialBrowser,
  getSocialContext,
  getSocialPage,
  getSessionStatus,
} from './session/manager.js';

// Graceful shutdown
export { trackContext, untrackContext } from './session/shutdown.js';

// Platform registry (session/login layer)
export { getPlatform, listPlatforms } from './platforms/registry.js';

// Publishing
export { SocialPublisher } from './publish/publisher.js';
export { getAdapter, getAllAdapters } from './publish/adapters/registry.js';
export { validateMediaFile, validateImages, validateVideos } from './publish/media.js';

// Types – session layer
export type {
  SocialPlatform,
  SocialPost,
  PostResult,
  SessionStatus,
} from './platforms/types.js';

// Types – publish layer
export type {
  SocialPlatformName,
  SocialPlatformAdapter,
  PublishPost,
  PublishResult,
  PublishOperation,
  PublishStatus,
  PublishOptions,
} from './publish/types.js';
export { PLATFORM_NAMES, isPlatformName } from './publish/types.js';

export type { MediaFile } from './publish/media.js';

// Errors – base + session
export {
  SocialAutomationError,
  InvalidPlatformError,
  ProfileNotFoundError,
  SessionExpiredError,
  LoginTimeoutError,
  BrowserLaunchError,
  NavigationTimeoutError,
} from './errors.js';

// Errors – publish
export {
  AuthenticationError,
  ComposerError,
  MediaValidationError,
  MediaUploadError,
  PublishError,
  VerificationError,
} from './publish/errors.js';

// Config
export { Config } from './config.js';
export type { SocialConfig } from './config.js';
