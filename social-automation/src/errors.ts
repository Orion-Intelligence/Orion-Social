
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
  constructor(platform: string, profilePath: string) {
    super(
      'PROFILE_NOT_FOUND',
      `Profile directory for "${platform}" not found at: ${profilePath}. Run the login command first.`,
    );
    this.name = 'ProfileNotFoundError';
  }
}

export class SessionExpiredError extends SocialAutomationError {
  constructor(platform: string) {
    super(
      'SESSION_EXPIRED',
      `Session for "${platform}" has expired or is invalid. ` +
      `Please re-authenticate: npm run social:login -- --platform ${platform}`,
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
