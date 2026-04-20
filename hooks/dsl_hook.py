import shutil
from pathlib import Path


def on_pre_build(config):
    src = Path("src/copia/data/dsl.md")
    dest = Path("docs/dsl.md")
    shutil.copy(src, dest)