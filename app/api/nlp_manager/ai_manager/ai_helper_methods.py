class ai_helper_methods:
    @staticmethod
    def strip_common_prefixes(text: str) -> str:
        t = text.lstrip()
        l = t.lower()
        prefixes = [
            "executive summary:", "summary:", "here is the summary:", "here's the summary:",
            "sure, here's the summary:", "sure:", "summary -", "summary —"
        ]
        for p in prefixes:
            if l.startswith(p):
                return t[len(p):].lstrip()
        return t
