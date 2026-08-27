import { SocialAutomationError } from '../errors.js';

export class AuthenticationError extends SocialAutomationError {
  constructor(platform: string) {
    super(
      'AUTHENTICATION_FAILED',
      `Not authenticated on "${platform}". ` +
      `Please run: npm run social:login -- --platform ${platform}`,
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
