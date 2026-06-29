import json
import shutil
import zipfile
from pathlib import Path


class BrowserSessionManager:
    def __init__(self, model):
        self.model = model

    def save(self, context):
        if not context:
            return
        self.prepare()
        path = self.state_path()
        context.storage_state(path=str(path))
        print(f"Session saved: {path}")
        print(f"Session folder: {self.path()}")

    def path(self):
        model_name = self.model.__class__.__name__
        session_name = model_name if model_name == "_facebook" else model_name.lstrip("_")
        return Path(__file__).resolve().parents[1] / f"{session_name}_session"

    def zip_path(self):
        return Path(str(self.path()) + ".zip")

    def state_path(self):
        return self.path() / "state.json"

    def profile_path(self):
        return self.path()

    def reset(self):
        path = self.path()
        zip_path = self.zip_path()
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
        elif path.exists():
            path.unlink()
        if zip_path.exists():
            zip_path.unlink()

    def restore_storage_state(self):
        self.prepare()
        path = self.state_path()
        return str(path) if path.is_file() else None

    def restore_context(self, context):
        path = self.restore_storage_state()
        if not path:
            return
        try:
            with open(path, encoding="utf-8") as session_file:
                storage_state = json.load(session_file)
            cookies = storage_state.get("cookies") or []
            if cookies:
                context.add_cookies(cookies)
            origins = storage_state.get("origins") or []
            if origins:
                origin_state = json.dumps(origins)
                context.add_init_script(f"""
                    (() => {{
                        const origins = {origin_state};
                        const origin = origins.find((entry) => entry.origin === window.location.origin);
                        if (!origin || !origin.localStorage) {{
                            return;
                        }}
                        for (const item of origin.localStorage) {{
                            window.localStorage.setItem(item.name, item.value);
                        }}
                    }})();
                """)
        except Exception:
            print(f"Could not load session state: {path}")

    def prepare(self):
        self._migrate_session_file()
        self._restore_zip()
        self._migrate_session_file()
        self.path().mkdir(parents=True, exist_ok=True)
        self._migrate_legacy_profile()

    def archive(self):
        path = self.path()
        if not path.is_dir():
            return
        zip_path = self.zip_path()
        if zip_path.exists():
            zip_path.unlink()
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
            for item in path.rglob("*"):
                archive_name = item.relative_to(path)
                if item.is_dir():
                    archive.write(item, f"{archive_name}/")
                elif item.is_file():
                    archive.write(item, archive_name)
        print(f"Session archive saved: {self.zip_path()}")

    def _migrate_session_file(self):
        path = self.path()
        if not path.is_file():
            return
        temp_path = Path(str(path) + "_state")
        if temp_path.exists():
            if temp_path.is_dir():
                shutil.rmtree(temp_path, ignore_errors=True)
            else:
                temp_path.unlink()
        path.rename(temp_path)
        path.mkdir(parents=True, exist_ok=True)
        shutil.move(str(temp_path), str(self.state_path()))

    def _restore_zip(self):
        path = self.path()
        zip_path = self.zip_path()
        if path.exists() or not zip_path.is_file():
            return
        with zipfile.ZipFile(zip_path) as archive:
            names = [name for name in archive.namelist() if name and not name.endswith("/")]
            wrapped = bool(names) and all(name.startswith(f"{path.name}/") for name in names)
        if wrapped:
            shutil.unpack_archive(str(zip_path), str(path.parent), "zip")
        else:
            path.mkdir(parents=True, exist_ok=True)
            shutil.unpack_archive(str(zip_path), str(path), "zip")

    def _legacy_profile_paths(self):
        path = self.path()
        paths = [Path(str(path) + "_profile")]
        if path.name.endswith("_session"):
            paths.append(path.with_name(f"{path.name[:-8]}_profile"))
        return paths

    def _migrate_legacy_profile(self):
        path = self.path()
        if (path / "Default").exists() or (path / "Local State").exists():
            return
        for legacy_path in self._legacy_profile_paths():
            if legacy_path.is_dir() and legacy_path != path:
                try:
                    shutil.copytree(
                        legacy_path,
                        path,
                        dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("Singleton*"),
                        ignore_dangling_symlinks=True,
                    )
                except shutil.Error:
                    pass
                return
