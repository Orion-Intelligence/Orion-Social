import type { AutomationResult } from '../../shared/model/models.js';

export interface DetectedAd {
  url: string;
  author: string;
  content_text: string;
  metadata: string;
  likes: string;
  shares: string;
  views: string;
  detected_at: string;
}

export interface AdDetectionResult extends AutomationResult {
  total_detected_ads: number;
  ads: DetectedAd[];
}
