import socket
import subprocess
import platform
from typing import Dict, Optional, TypedDict
from threading import Lock


class ScanResult(TypedDict):
	ip: str
	hostname: Optional[str]
	ping: Optional[bool]


class IPScanner:
	def __init__(self):
		self._states: Dict[str, Dict] = {}
		self._lock = Lock()

	def _set_state(self, ip: str, **kwargs):
		with self._lock: self._states.setdefault(ip, {"status": "pending", "progress": 0, "step": "queued", "result": None}).update(kwargs)

	def get_ip_scan_status(self, ip: str) -> Dict:
		with self._lock: return self._states.get(ip, {"status": "idle", "progress": 0, "step": ""})

	def _tcp_ping(self, ip: str, port: int = 80, timeout: float = 2.0) -> bool:
		try:
			with socket.create_connection((ip, port), timeout=timeout): return True
		except Exception: return False

	def _get_hostname(self, ip: str) -> str:
		try: return socket.gethostbyaddr(ip)[0]
		except Exception:
			try:
				r = subprocess.run(["dnsx", "-ptr", "-silent", "-resp", ip], capture_output=True, text=True, timeout=8)
				if r.returncode == 0 and r.stdout.strip(): return r.stdout.strip().splitlines()[0].rstrip(".")
			except Exception: pass
		return "Unknown"

	def run_ip_scan(self, ip: str):
		try:
			self._set_state(ip, status="pending", progress=5, step="queued")
			result: ScanResult = {"ip": ip, "hostname": None, "ping": None}
			self._set_state(ip, progress=30, step="hostname_lookup")
			result["hostname"] = self._get_hostname(ip)
			self._set_state(ip, progress=60, step="ping_check")
			try:
				param = "-n" if platform.system().lower() == "windows" else "-c"
				result["ping"] = subprocess.run(["ping", param, "1", ip], capture_output=True, text=True, timeout=6).returncode == 0
			except Exception: result["ping"] = False
			if not result["ping"]: result["ping"] = self._tcp_ping(ip)
			self._set_state(ip, status="done", progress=100, step="done", result=result)
		except Exception as e:
			self._set_state(ip, status="error", progress=100, step="error", result={"error": str(e)})
