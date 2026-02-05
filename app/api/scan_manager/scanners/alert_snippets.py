
class AlertSnippets:
    @staticmethod
    def augment(zap, baseurl: str, alert: dict) -> str:
        evidence = alert.get("evidence","") or ""
        chunk = ""
        try:
            mid = alert.get("messageId") or alert.get("messageid")
            if not mid:
                lst = alert.get("messageIdList") or alert.get("messageidlist") or []
                mid = lst[0] if lst else None
            if mid:
                full = zap.core.message(int(mid))
                res_hdr = full.get("responseHeader","") or ""
                res_body = full.get("responseBody","") or ""
                target = res_body if res_body else res_hdr
                if target:
                    if evidence:
                        i = target.find(evidence)
                        if i >= 0:
                            a = max(0, i-160); b = min(len(target), i+len(evidence)+160)
                            chunk = target[a:b]
                        else:
                            chunk = target[:600]
                    else:
                        chunk = target[:600]
        except Exception:
            pass
        if not chunk and evidence:
            chunk = evidence[:600]
        return chunk
