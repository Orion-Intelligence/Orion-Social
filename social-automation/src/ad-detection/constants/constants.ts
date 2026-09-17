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
  const originalPush = result.ads.push.bind(result.ads);
  result.ads.push = function(...args) {
    const ret = originalPush(...args);
    result.total_detected_ads = result.ads.length;
    if (result.ads.length >= 8) {
      console.log('[Automation] Maximum ad limit (8) reached. Stopping script gracefully.');
      const resultFile = (global as any).RESULT_FILE;
      if (resultFile) {
        const fs = require('fs');
        fs.writeFileSync(resultFile, JSON.stringify(result, null, 2), 'utf-8');
      }
      process.exit(0);
    }
    return ret;
  };

  return result;
}
