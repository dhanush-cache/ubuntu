import tarfile
from pathlib import Path
from shutil import rmtree
from tempfile import NamedTemporaryFile, TemporaryDirectory
from zipfile import ZipFile

import requests

from config import HOME

THEMES = HOME / ".themes"
CONFIGS = HOME / ".config"


def download_theme(url: str, name: str):
    target = THEMES / name
    rmtree(target, ignore_errors=True)

    response = requests.get(url)
    source = NamedTemporaryFile(suffix=".zip")
    extraxt_dir = TemporaryDirectory(delete=False)

    source.write(response.content)
    archive = None
    try:
        archive = (
            tarfile.open(source.name, mode="r:xz")
            if url.endswith(".xz")
            else ZipFile(source)
        )
        archive.extractall(extraxt_dir.name)
    finally:
        if archive is not None:
            archive.close()
    source = next(
        file for file in Path(extraxt_dir.name).rglob("*") if "gtk-4.0" in file.name
    ).parent
    THEMES.mkdir(parents=True, exist_ok=True)
    source.rename(target)
    configure(target)


def configure(theme_dir: Path):
    paths = [
        "gtk-4.0/gtk.css",
        "gtk-4.0/gtk-dark.css",
        "gtk-4.0/assets",
        "assets",
    ]
    for path in paths:
        source = theme_dir / path
        target = CONFIGS / path

        target.unlink(missing_ok=True)
        rmtree(target, ignore_errors=True)

        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(source)


def main():
    url = "https://github.com/dracula/gtk/archive/master.zip"
    name = "Dracula"
    download_theme(url, name)
    url = "https://github.com/catppuccin/gtk/releases/latest/download/catppuccin-mocha-blue-standard+default.zip"
    name = "Catppuccin"
    download_theme(url, name)


if __name__ == "__main__":
    main()
