import fs from 'node:fs';
import path from 'node:path';
import { MediaValidationError } from '../../shared/errors.js';
import type { MediaFile } from '../model/models.js';
import { IMAGE_EXTENSIONS, MAX_FILE_SIZE_BYTES } from '../constants/constants.js';

export class MediaValidator {
  validateMediaFile(filePath: string, supportedExtensions?: readonly string[]): MediaFile {
    const absolutePath = path.resolve(filePath);
    const ext = path.extname(absolutePath).toLowerCase();

    if (!fs.existsSync(absolutePath)) {
      throw new MediaValidationError(`File does not exist: ${absolutePath}`);
    }

    try {
      fs.accessSync(absolutePath, fs.constants.R_OK);
    } catch {
      throw new MediaValidationError(`File is not readable: ${absolutePath}`);
    }

    if (!IMAGE_EXTENSIONS.has(ext)) {
      throw new MediaValidationError(
        `Unsupported file extension "${ext}" for: ${absolutePath}. ` +
        `Supported: ${[...IMAGE_EXTENSIONS].join(', ')}`,
      );
    }

    if (supportedExtensions && !supportedExtensions.includes(ext)) {
      throw new MediaValidationError(
        `Extension "${ext}" is not supported by this platform. ` +
        `Supported: ${supportedExtensions.join(', ')}`,
      );
    }

    const stat = fs.statSync(absolutePath);
    if (stat.size === 0) {
      throw new MediaValidationError(`File is empty: ${absolutePath}`);
    }
    if (stat.size > MAX_FILE_SIZE_BYTES) {
      throw new MediaValidationError(
        `File too large (${(stat.size / 1024 / 1024).toFixed(1)} MB): ${absolutePath}. ` +
        `Maximum: ${MAX_FILE_SIZE_BYTES / 1024 / 1024} MB`,
      );
    }

    return {
      absolutePath,
      extension: ext,
      sizeBytes: stat.size,
      type: 'image',
    };
  }

  validateImages(images: readonly string[], supportedExtensions: readonly string[], maxCount: number): MediaFile[] {
    if (images.length > maxCount) {
      throw new MediaValidationError(
        `Too many images: ${images.length}. This platform supports at most ${maxCount}.`,
      );
    }
    return images.map((img) => this.validateMediaFile(img, supportedExtensions));
  }
}
