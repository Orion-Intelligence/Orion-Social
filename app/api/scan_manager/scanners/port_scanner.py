import socket, select

class port_scanner:
    def __init__(self, ports=None, timeout=1.0):
        default_ports = [
            21,22,23,25,53,80,110,143,389,443,445,465,587,993,995,
            1433,1521,2049,2375,2376,3000,3306,3389,4444,5432,5601,5900,
            6379,7001,8000,8008,8080,8081,8443,9000,9200,9300,11211,27017
        ]
        self.ports = list(dict.fromkeys((ports or default_ports)))
        self.timeout = timeout
        self.sev_high = {21,23,25,110,143,389,445,1433,1521,2049,2375,2376,3306,3389,5432,5900,6379,7001,9200,9300,11211,27017}

    def scan(self, host, add_cb, progress_cb=None, start=75, end=90):
        if not host:
            return
        n = len(self.ports)
        span = max(1, end - start)
        for i, p in enumerate(self.ports, 1):
            if progress_cb:
                pct = start + int(i * span / n)
                progress_cb(pct, f"network_checks:port_scan:{p}")
            try:
                with socket.create_connection((host, p), timeout=self.timeout) as s:
                    s.setblocking(0)
                    banner = ""
                    try:
                        r,_,_ = select.select([s], [], [], 0.25)
                        if r:
                            try:
                                banner = s.recv(256).decode(errors="ignore").strip()
                            except Exception:
                                banner = ""
                    except Exception:
                        banner = ""
                    risk = "High" if p in self.sev_high else "Medium"
                    desc = f"TCP {p} open" + (f"; banner: {banner}" if banner else "")
                    add_cb("Port Scan", f"Open Port {p}", desc, "High", risk)
            except Exception:
                continue
        if progress_cb:
            progress_cb(end, "network_checks:port_scan_done")
