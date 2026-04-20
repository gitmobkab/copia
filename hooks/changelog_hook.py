import shutil
from pathlib import Path


def on_pre_build(config):
    src = Path("CHANGELOG.md")
    dest = Path("docs/changelog.md")
    if src.exists():
        shutil.copy(src, dest)