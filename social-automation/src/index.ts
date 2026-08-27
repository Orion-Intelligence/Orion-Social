
export {
  getSocialBrowser,
  getSocialContext,
  getSocialPage,
  getSessionStatus,
} from './session/manager.js';

export { trackContext, untrackContext } from './session/shutdown.js';

export { getPlatform, listPlatforms } from './platforms/registry.js';

export { SocialPublisher } from './publish/publisher.js';
export { getAdapter, getAllAdapters } from './publish/adapters/registry.js';
export { validateMediaFile, validateImages, validateVideos } from './publish/media.js';

export type {
  SocialPlatform,
  SocialPost,
  PostResult,
  SessionStatus,
} from './platforms/types.js';

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

export {
  SocialAutomationError,
  InvalidPlatformError,
  ProfileNotFoundError,
  SessionExpiredError,
  LoginTimeoutError,
  BrowserLaunchError,
  NavigationTimeoutError,
} from './errors.js';

export {
  AuthenticationError,
  ComposerError,
  MediaValidationError,
  MediaUploadError,
  PublishError,
  VerificationError,
} from './publish/errors.js';

export { Config } from './config.js';
export type { SocialConfig } from './config.js';
