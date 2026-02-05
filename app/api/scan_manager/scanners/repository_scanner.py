import json, re, shutil, subprocess, tempfile
from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path
from fastapi import HTTPException


class repository_scanner:
    @staticmethod
    def _run(cmd, timeout=600):
        try:
            r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)
            return r.returncode, r.stdout, r.stderr
        except Exception:
            raise HTTPException(status_code=500, detail="Something unexpected happened")

    @staticmethod
    def _normalize(repo: str):
        repo = repo.strip()
        if re.match(r"^[\w\-.]+/[\w\-.]+$", repo):
            return f"https://github.com/{repo}.git"
        patterns = {
            "github": r"github\.com[:/]{1,2}([^/]+/[^/]+)",
            "gitlab": r"gitlab\.com[:/]{1,2}([^/]+/[^/]+)",
            "bitbucket": r"bitbucket\.org[:/]{1,2}([^/]+/[^/]+)",
            "sourceforge": r"sourceforge\.net[:/]{1,2}([^/]+/[^/]+)",
            "gitea": r"gitea\.com[:/]{1,2}([^/]+/[^/]+)",
            "codeberg": r"codeberg\.org[:/]{1,2}([^/]+/[^/]+)",
            "azure": r"dev\.azure\.com[:/]{1,2}([^/]+/[^/]+)",
        }
        bases = {
            "github": "https://github.com",
            "gitlab": "https://gitlab.com",
            "bitbucket": "https://bitbucket.org",
            "sourceforge": "https://sourceforge.net/p",
            "gitea": "https://gitea.com",
            "codeberg": "https://codeberg.org",
            "azure": "https://dev.azure.com",
        }
        for p, r in patterns.items():
            m = re.search(r, repo)
            if m:
                return f"{bases[p]}/{m.group(1)}.git"
        raise HTTPException(status_code=500, detail="Something unexpected happened")

    def _dir_size_mb(self, path: Path) -> float:
        total = 0
        for p in path.rglob("*"):
            try:
                if p.is_file():
                    total += p.stat().st_size
            except Exception:
                pass
        return total / (1024 * 1024)

    @staticmethod
    def _host_from_url(u: str) -> str:
        try:
            return (urlparse(u).hostname or "").strip()
        except Exception:
            return ""

    @staticmethod
    def _http_port_for(url: str) -> str:
        try:
            p = urlparse(url)
            if (p.scheme or "").lower().startswith("http"):
                return "443 SSL" if (p.scheme.lower() == "https") else "80"
        except Exception:
            pass
        return "443 SSL"

    @staticmethod
    def _risk_title(s: str) -> str:
        return (s or "").strip().capitalize()

    def parse(self, repo_input: str, timeout=900, progress_cb=None, scanner_name: str = "Orion Intelligence"):
        if progress_cb:
            try:
                progress_cb(5, "resolving")
            except Exception:
                pass
        if repo_input.endswith(".zip"):
            raise HTTPException(status_code=500, detail="Something unexpected happened")
        script_dir = Path(__file__).resolve().parent
        tmp_root = script_dir / "tmp_scans"
        tmp_root.mkdir(parents=True, exist_ok=True)
        temp_dir = Path(tempfile.mkdtemp(prefix="repo_scan_", dir=tmp_root))
        repo_dir = temp_dir / "repo"
        try:
            repo_url = self._normalize(repo_input)
            if progress_cb:
                try:
                    progress_cb(10, "cloning")
                except Exception:
                    pass
            c, o, e = self._run(["git", "clone", "--depth", "1", repo_url, str(repo_dir)], timeout=max(60, timeout // 10))
            if c != 0 or not repo_dir.exists():
                raise HTTPException(status_code=500, detail="Something unexpected happened")
            if progress_cb:
                try:
                    progress_cb(25, "sizing")
                except Exception:
                    pass
            size_mb = self._dir_size_mb(repo_dir)
            if size_mb > 500:
                raise HTTPException(status_code=500, detail="Repository too large")
            trivy_path = shutil.which("trivy")
            if not trivy_path:
                raise HTTPException(status_code=500, detail="Something unexpected happened")
            if progress_cb:
                try:
                    progress_cb(50, "scanning")
                except Exception:
                    pass
            c, o, e = self._run([
                trivy_path, "fs", "--no-progress", "--quiet", "--format", "json",
                "--scanners", "vuln,secret,misconfig,license",
                "--severity", "HIGH,CRITICAL", str(repo_dir)
            ], timeout=timeout)
            if c not in (0, 2):
                raise HTTPException(status_code=500, detail="Something unexpected happened")
            try:
                trivy_json = json.loads(o)
            except Exception:
                raise HTTPException(status_code=500, detail="Something unexpected happened")
            if progress_cb:
                try:
                    progress_cb(80, "aggregating")
                except Exception:
                    pass
            categories = {
                "Vulnerabilities": [],
                "Misconfigurations": [],
                "Secrets": [],
                "Licenses": [],
            }
            proofs = {k: [] for k in categories.keys()}

            def add_threat(cat, header, description, confidence, risk, proof=None):
                categories[cat].append({
                    "header": header,
                    "description": description,
                    "confidence": confidence,
                    "risk": risk
                })
                if proof:
                    proofs[cat].append({
                        "header": header,
                        "proof": proof,
                        "confidence": confidence,
                        "risk": risk
                    })

            results = trivy_json if isinstance(trivy_json, list) else trivy_json.get("Results") or []
            for r in results:
                target = r.get("Target") or ""
                for v in (r.get("Vulnerabilities") or []):
                    sev = self._risk_title(v.get("Severity"))
                    header = v.get("VulnID") or v.get("Title") or "Vulnerability"
                    pkg = v.get("PkgName") or ""
                    iv = v.get("InstalledVersion") or ""
                    fv = v.get("FixedVersion") or ""
                    desc = v.get("Title") or v.get("Description") or ""
                    info_parts = []
                    if pkg:
                        info_parts.append(f"Package: {pkg}")
                    if iv:
                        info_parts.append(f"Installed: {iv}")
                    if fv:
                        info_parts.append(f"Fixed: {fv}")
                    info = (" | ".join(info_parts)).strip()
                    proof = f"Target: {target}\n{info}".strip()
                    conf = v.get("Confidence") or ("High" if sev == "Critical" else "Medium")
                    add_threat("Vulnerabilities", header, desc, conf, sev, proof=proof)
                for m in (r.get("Misconfigurations") or []):
                    sev = self._risk_title(m.get("Severity"))
                    header = m.get("ID") or m.get("Title") or "Misconfiguration"
                    desc = m.get("Title") or m.get("Message") or m.get("Description") or ""
                    proof = f"Target: {target}\nCheck: {m.get('CheckID') or ''}\nCause: {m.get('CauseMetadata') or ''}".strip()
                    conf = m.get("Confidence") or ("High" if sev == "Critical" else "Medium")
                    add_threat("Misconfigurations", header, desc, conf, sev, proof=proof)
                for s in (r.get("Secrets") or []):
                    sev = self._risk_title(s.get("Severity") or "High")
                    header = s.get("RuleID") or "Secret Detected"
                    desc = s.get("Title") or s.get("Description") or "Potential secret detected in the repository."
                    proof = f"Target: {target}\nMatch: {s.get('Match') or ''}\nFile: {s.get('FilePath') or ''}".strip()
                    conf = s.get("Confidence") or "High"
                    add_threat("Secrets", header, desc, conf, sev, proof=proof)
                for l in (r.get("Licenses") or []):
                    sev = self._risk_title(l.get("Severity") or "High")
                    header = l.get("PkgName") or "License Issue"
                    desc = l.get("Title") or l.get("License") or "License finding"
                    pkg = l.get("PkgName") or ""
                    lic = l.get("License") or ""
                    proof = f"Target: {target}\nPackage: {pkg}\nLicense: {lic}".strip()
                    conf = l.get("Confidence") or "Medium"
                    add_threat("Licenses", header, desc, conf, sev, proof=proof)
            summary = {k: len(v) for k, v in categories.items() if v}
            high = sum(1 for lst in categories.values() for t in lst if (t.get("risk") or "").lower() in ("high", "critical"))
            medium = sum(1 for lst in categories.values() for t in lst if (t.get("risk") or "").lower() == "medium")
            low = sum(1 for lst in categories.values() for t in lst if (t.get("risk") or "").lower() == "low")
            info = sum(1 for lst in categories.values() for t in lst if (t.get("risk") or "").lower() == "informational")
            if high > 0:
                grade = "F"
            elif medium >= 5:
                grade = "D"
            elif medium >= 1:
                grade = "C"
            elif low > 0:
                grade = "B"
            else:
                grade = "A"
            display_url = repo_input.strip()
            if display_url.endswith(".git"):
                display_url = display_url[:-4]
            if "://" not in display_url:
                display_url = self._normalize(repo_input)[:-4]
            host = self._host_from_url(self._normalize(repo_input)) or "unknown"
            meta = {
                "URL": display_url,
                "Host": host,
                "Port": self._http_port_for(self._normalize(repo_input)),
                "Scanned_on_date": datetime.now().strftime("%B %d, %Y"),
                "Scanned_by": scanner_name
            }
            result = {
                "meta": meta,
                "summary": summary,
                "threats": {k: v for k, v in categories.items() if v},
                "proofs": {k: v for k, v in proofs.items() if v},
                "grade": grade,
                "grade_counts": {
                    "high": high,
                    "medium": medium,
                    "low": low,
                    "informational": info
                }
            }
            if progress_cb:
                try:
                    progress_cb(95, "finalizing")
                except Exception:
                    pass
            if progress_cb:
                try:
                    progress_cb(100, "complete")
                except Exception:
                    pass
            return result
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
