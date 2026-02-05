from api.scan_manager.helpers.utils import header_present


class HeaderChecks:
    @staticmethod
    def check(res_hdr: str, add):
        checks = [
            ("Strict-Transport-Security","Missing HSTS; enable for HTTPS sites"),
            ("X-Frame-Options","Missing X-Frame-Options; consider 'DENY' or 'SAMEORIGIN'"),
            ("X-Content-Type-Options","Missing X-Content-Type-Options; use 'nosniff'"),
            ("Referrer-Policy","Missing Referrer-Policy"),
            ("Permissions-Policy","Missing Permissions-Policy"),
            ("Cross-Origin-Resource-Policy","Missing CORP"),
            ("Cross-Origin-Opener-Policy","Missing COOP"),
            ("Cross-Origin-Embedder-Policy","Missing COEP"),
            ("Cache-Control","Missing/weak Cache-Control"),
        ]
        for name, msg in checks:
            if not header_present(res_hdr, name):
                add("Headers", name, msg, "High", "Medium")
        if header_present(res_hdr, "Content-Security-Policy-Report-Only") and not header_present(res_hdr, "Content-Security-Policy"):
            add("Headers", "Content-Security-Policy-Report-Only", "CSP is report-only; consider enforcing", "Medium", "Low")
