import { SocialAutomationError } from '../errors.js';

/** The session is not authenticated for the target platform. */
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

/** The post composer could not be opened or is in an unexpected state. */
export class ComposerError extends SocialAutomationError {
  constructor(platform: string, detail: string) {
    super(
      'COMPOSER_ERROR',
      `Failed to open composer on ${platform}: ${detail}`,
    );
    this.name = 'ComposerError';
  }
}

/** A media file failed validation (missing, unsupported, too large, etc.). */
export class MediaValidationError extends SocialAutomationError {
  constructor(detail: string) {
    super('MEDIA_VALIDATION_ERROR', detail);
    this.name = 'MediaValidationError';
  }
}

/** Media upload failed during the publish workflow. */
export class MediaUploadError extends SocialAutomationError {
  constructor(platform: string, detail: string) {
    super(
      'MEDIA_UPLOAD_ERROR',
      `Media upload failed on ${platform}: ${detail}`,
    );
    this.name = 'MediaUploadError';
  }
}

/** The publish button click or submission failed. */
export class PublishError extends SocialAutomationError {
  constructor(platform: string, detail: string) {
    super(
      'PUBLISH_ERROR',
      `Publish failed on ${platform}: ${detail}`,
    );
    this.name = 'PublishError';
  }
}

/** Post-publish verification could not confirm the post was created. */
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
