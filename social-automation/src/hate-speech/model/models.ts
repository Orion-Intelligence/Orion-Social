import type { AutomationResult } from '../../shared/model/models.js';

export interface ExtractedPost {
  url: string;
  author: string;
  content_text: string;
  detected_at: string;
  likes?: string;
  shares?: string;
  views?: string;
}

export interface HateSpeechMonitorResult extends AutomationResult {
  total_posts: number;
  hate_posts_count: number;
  posts: ExtractedPost[];
}
