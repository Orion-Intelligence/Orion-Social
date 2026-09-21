import type { AdDetectionResult } from '../model/models.js';

export const MAX_SCROLLS = 50;

export function createEmptyAdDetectionResult(): AdDetectionResult {
  return {
    total_detected_ads: 0,
    ads: [],
    error: false,
    error_reason: '',
    session_expired: false,
  };
}
