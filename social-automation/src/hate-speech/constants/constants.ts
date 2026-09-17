import type { HateSpeechMonitorResult } from '../model/models.js';

export function createEmptyHateSpeechMonitorResult(): HateSpeechMonitorResult {
  return {
    error: false,
    session_expired: false,
    error_reason: '',
    total_posts: 0,
    hate_posts_count: 0,
    posts: [],
  };
}
