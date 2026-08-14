class helper_method:
    @staticmethod
    def normalize_platform(platform: str) -> str:
        value = str(platform or "").strip().lower()
        return "x" if value == "twitter" else value
