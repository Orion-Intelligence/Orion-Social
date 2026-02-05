
import re

class PIIChecks:
    @staticmethod
    def _mask(s: str, keep_last: int = 4) -> str:
        digits = [c for c in s if c.isdigit()]
        if not digits: return s
        n = len(digits); keep = max(0, min(keep_last, n))
        masked_digits = ["*" for _ in range(n-keep)] + digits[-keep:]
        out, idx = [], 0
        for ch in s:
            if ch.isdigit():
                out.append(masked_digits[idx]); idx += 1
            else:
                out.append(ch)
        return "".join(out)

    @staticmethod
    def check(res_hdr: str, res_body: str, add):
        body = res_body or ""
        re_email = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
        for m in re_email.finditer(body):
            s = m.group(0)
            left, dom = s.split("@",1)
            masked = (left[0] + "***" + (left[-1] if len(left)>1 else "")) + "@" + dom
            add("PII","Email Address",masked,"Medium","Low")
        for m in re.finditer(r"\b(?:\d[ -]*?){13,19}\b", body):
            raw = m.group(0)
            masked = PIIChecks._mask(raw, keep_last=4)
            add("PII","Credit Card Number",masked,"High","High")
