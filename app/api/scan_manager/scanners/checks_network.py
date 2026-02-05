
import ssl, socket
from datetime import datetime

class NetworkChecks:
    @staticmethod
    def tls_certificate(host, add, port=443, warn_days=30):
        try:
            ctx = ssl.create_default_context()
            with socket.create_connection((host, port), timeout=5) as sock:
                with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
            not_after = cert.get("notAfter","")
            if not_after:
                exp = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                days = (exp - datetime.utcnow()).days
                if days < warn_days:
                    add("TLS","Certificate Expiry",f"Certificate expires in {days} day(s)","High","Medium")
            subject = dict(x for xs in cert.get("subject", []) for x in xs).get("commonName","")
            issuer = dict(x for xs in cert.get("issuer", []) for x in xs).get("commonName","")
            if subject and issuer and subject == issuer:
                add("TLS","Self-signed certificate?","Subject CN equals Issuer CN; verify chain","Medium","Low")
        except Exception:
            pass
