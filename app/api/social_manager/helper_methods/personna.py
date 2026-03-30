from rapidfuzz import fuzz


class personna:
    def __init__(self):
        self.weights = {
            "real_name": 0.24,
            "bio": 0.26,
            "location": 0.10,
            "profile_url": 0.10,
            "total_posts": 0.10,
            "total_followers": 0.10,
            "total_following": 0.10
        }

    def _normalize_text(self, value):
        if value is None:
            return ""
        return " ".join(str(value).strip().lower().split())

    def _text_similarity(self, value_1, value_2):
        left = self._normalize_text(value_1)
        right = self._normalize_text(value_2)

        if not left and not right:
            return 100.0
        if not left or not right:
            return 0.0

        return float(fuzz.ratio(left, right))

    def _to_number(self, value):
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)

        cleaned = "".join(ch for ch in str(value) if ch.isdigit() or ch == ".")
        if not cleaned:
            return None

        try:
            return float(cleaned)
        except ValueError:
            return None

    def _numeric_similarity(self, value_1, value_2):
        left = self._to_number(value_1)
        right = self._to_number(value_2)

        if left is None and right is None:
            return 100.0
        if left is None or right is None:
            return 0.0

        baseline = max(abs(left), abs(right), 1.0)
        distance = abs(left - right)
        score = 100.0 * (1.0 - (distance / baseline))

        return max(score, 0.0)

    def _to_profile_dict(self, profile):
        if profile is None:
            return {}
        if isinstance(profile, dict):
            return profile
        if hasattr(profile, "model_dump"):
            return profile.model_dump()
        return {}

    def compare_profiles(self, profile_1, profile_2):
        profile_1 = self._to_profile_dict(profile_1)
        profile_2 = self._to_profile_dict(profile_2)

        field_scores = {
            "real_name": round(self._text_similarity(profile_1.get("real_name"), profile_2.get("real_name")), 2),
            "bio": round(self._text_similarity(profile_1.get("bio"), profile_2.get("bio")), 2),
            "location": round(self._text_similarity(profile_1.get("location"), profile_2.get("location")), 2),
            "profile_url": round(self._text_similarity(profile_1.get("profile_url"), profile_2.get("profile_url")), 2),
            "total_posts": round(self._numeric_similarity(profile_1.get("total_posts"), profile_2.get("total_posts")), 2),
            "total_followers": round(self._numeric_similarity(profile_1.get("total_followers"), profile_2.get("total_followers")), 2),
            "total_following": round(self._numeric_similarity(profile_1.get("total_following"), profile_2.get("total_following")), 2)
        }

        overall = 0.0
        for field, weight in self.weights.items():
            overall += field_scores[field] * weight

        return {
            "field_similarity": field_scores,
            "overall_similarity": round(overall, 2)
        }

    def estimate_original_profile(self, profile_1, profile_2):
        profile_1 = self._to_profile_dict(profile_1)
        profile_2 = self._to_profile_dict(profile_2)

        def profile_strength(profile):
            posts = self._to_number(profile.get("total_posts")) or 0.0
            followers = self._to_number(profile.get("total_followers")) or 0.0
            following = self._to_number(profile.get("total_following")) or 0.0
            completeness = 0
            for key in ("real_name", "bio", "location", "profile_url"):
                if self._normalize_text(profile.get(key)):
                    completeness += 1

            return (followers * 0.5) + (following * 0.2) + (posts * 0.3) + (completeness * 50)

        score_1 = profile_strength(profile_1)
        score_2 = profile_strength(profile_2)

        if score_1 >= score_2:
            return profile_1.get("profile_url") or ""
        return profile_2.get("profile_url") or ""