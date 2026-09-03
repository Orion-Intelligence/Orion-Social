
export class SocialAutomationError extends Error {
  public readonly code: string;

  constructor(code: string, message: string) {
    super(message);
    this.name = 'SocialAutomationError';
    this.code = code;
  }
}

export class InvalidPlatformError extends SocialAutomationError {
  constructor(platform: string) {
    super(
      'INVALID_PLATFORM',
      `Unknown social platform "${platform}". Use one of the registered platform identifiers.`,
    );
    this.name = 'InvalidPlatformError';
  }
}

export class ProfileNotFoundError extends SocialAutomationError {
  constructor(platform: string, _profilePath: string) {
    super(
      'PROFILE_NOT_FOUND',
      `Profile data for "${platform}" not found. Please provide a valid session state.`,
    );
    this.name = 'ProfileNotFoundError';
  }
}

export class SessionExpiredError extends SocialAutomationError {
  constructor(platform: string) {
    super(
      'SESSION_EXPIRED',
      `Session for "${platform}" has expired or is invalid. ` +
      `Please provide a valid session state for ${platform}.`,
    );
    this.name = 'SessionExpiredError';
  }
}

export class LoginTimeoutError extends SocialAutomationError {
  constructor(platform: string) {
    super(
      'LOGIN_TIMEOUT',
      `Login for "${platform}" was not completed within the allowed time. ` +
      'Please try again and complete authentication promptly.',
    );
    this.name = 'LoginTimeoutError';
  }
}

export class BrowserLaunchError extends SocialAutomationError {
  constructor(reason: string) {
    super(
      'BROWSER_LAUNCH_FAILED',
      `Failed to launch browser: ${reason}. ` +
      'Ensure Playwright browsers are installed: npx playwright install chromium',
    );
    this.name = 'BrowserLaunchError';
  }
}

export class NavigationTimeoutError extends SocialAutomationError {
  constructor(url: string, reason: string) {
    super(
      'NAVIGATION_TIMEOUT',
      `Navigation to ${url} timed out: ${reason}`,
    );
    this.name = 'NavigationTimeoutError';
  }
}

export class AuthenticationError extends SocialAutomationError {
  constructor(platform: string) {
    super(
      'AUTHENTICATION_FAILED',
      `Not authenticated on "${platform}". ` +
      `Please provide a valid session state for ${platform}.`,
    );
    this.name = 'AuthenticationError';
  }
}

export class ComposerError extends SocialAutomationError {
  constructor(platform: string, detail: string) {
    super(
      'COMPOSER_ERROR',
      `Failed to open composer on ${platform}: ${detail}`,
    );
    this.name = 'ComposerError';
  }
}

export class MediaValidationError extends SocialAutomationError {
  constructor(detail: string) {
    super('MEDIA_VALIDATION_ERROR', detail);
    this.name = 'MediaValidationError';
  }
}

export class MediaUploadError extends SocialAutomationError {
  constructor(platform: string, detail: string) {
    super(
      'MEDIA_UPLOAD_ERROR',
      `Media upload failed on ${platform}: ${detail}`,
    );
    this.name = 'MediaUploadError';
  }
}

export class PublishError extends SocialAutomationError {
  constructor(platform: string, detail: string) {
    super(
      'PUBLISH_ERROR',
      `Publish failed on ${platform}: ${detail}`,
    );
    this.name = 'PublishError';
  }
}

export class VerificationError extends SocialAutomationError {
  constructor(platform: string, detail: string) {
    super(
      'VERIFICATION_ERROR',
      `Post verification failed on ${platform}: ${detail}. ` +
      'The post may or may not have been published – check manually before retrying.',
    );
    this.name = 'VerificationError';
  }
}
