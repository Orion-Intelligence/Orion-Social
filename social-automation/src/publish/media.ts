import fs from 'node:fs';
import path from 'node:path';
import { MediaValidationError } from '../shared/errors.js';

const MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024;

const IMAGE_EXTENSIONS = new Set(['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']);
const VIDEO_EXTENSIONS = new Set(['.mp4', '.mov', '.avi', '.wmv', '.webm', '.mkv']);

export interface MediaFile {
  readonly absolutePath: string;
  readonly extension: string;
  readonly sizeBytes: number;
  readonly type: 'image' | 'video';
}

export function validateMediaFile(
  filePath: string,
  supportedExtensions?: readonly string[],
): MediaFile {
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

  const isImage = IMAGE_EXTENSIONS.has(ext);
  const isVideo = VIDEO_EXTENSIONS.has(ext);
  if (!isImage && !isVideo) {
    throw new MediaValidationError(
      `Unsupported file extension "${ext}" for: ${absolutePath}. ` +
      `Supported: ${[...IMAGE_EXTENSIONS, ...VIDEO_EXTENSIONS].join(', ')}`,
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
    type: isImage ? 'image' : 'video',
  };
}

export function validateImages(
  images: readonly string[],
  supportedExtensions: readonly string[],
  maxCount: number,
): MediaFile[] {
  if (images.length > maxCount) {
    throw new MediaValidationError(
      `Too many images: ${images.length}. This platform supports at most ${maxCount}.`,
    );
  }
  return images.map((img) => validateMediaFile(img, supportedExtensions));
}

export function validateVideos(
  videos: readonly string[],
  supportedExtensions: readonly string[],
): MediaFile[] {
  return videos.map((vid) => validateMediaFile(vid, supportedExtensions));
}
