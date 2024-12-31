__all__ = ["WORK_DIR", "SYNC_DIR"]

from pathlib import Path

WORK_DIR = (Path(__file__).parent / ".." / "..").resolve()
SYNC_DIR = Path("~/Sync/reMarkable").expanduser()
