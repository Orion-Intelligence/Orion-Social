import sys
from pathlib import Path

_social_manager_file = Path(__file__).resolve()
for _path in (_social_manager_file.parents[2], _social_manager_file.parents[3]):
    _path_str = str(_path)
    if (_path / "crawler").exists() and _path_str not in sys.path:
        sys.path.insert(0, _path_str)
