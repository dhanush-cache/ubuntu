"""Module to configure ubuntu's fonts and colors."""

import io
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import urlparse
from zipfile import ZipFile

import requests

from config import HOME

FONTS = HOME / ".fonts"

wallpaper = Path("/usr/share/backgrounds/clean-code.jpg")


def get_wallpaper():
    wallpaper_url = "https://quotefancy.com/media/wallpaper/3840x2160/1907616-Martin-Fowler-Quote-Any-fool-can-write-code-that-a-computer-can.jpg"
    if wallpaper.exists():
        return wallpaper
    file = NamedTemporaryFile(suffix=".jpg")
    response = requests.get(wallpaper_url)
    file.write(response.content)
    command = ["sudo", "mv", file.name, str(wallpaper)]
    subprocess.run(command)
    return wallpaper


gnome_configs = f"""[org/gnome/desktop/background]
picture-uri='{get_wallpaper()}'
picture-uri-dark='{get_wallpaper()}'

[org/gnome/desktop/input-sources]
xkb-options=['caps:ctrl_modifier']

[org/gnome/desktop/interface]
color-scheme='prefer-dark'

[org/gnome/desktop/wm/preferences]
num-workspaces=1

[org/gnome/mutter]
dynamic-workspaces=false

[org/gnome/shell]
favorite-apps=['org.gnome.Nautilus.desktop', 'firefox.desktop', 'code.desktop', 'Alacritty.desktop', 'org.gnome.Settings.desktop', 'jetbrains-toolbox.desktop', 'vlc_vlc.desktop']

[org/gnome/settings-daemon/plugins/media-keys]
control-center=['<Control><Alt>s']
home=['<Super>e']
www=['<Control><Alt>b']

[org/gnome/shell/extensions/dash-to-dock]
dash-max-icon-size=80
dock-fixed=false
dock-position='BOTTOM'
extend-height=false
multi-monitor=true
"""


def configure_gnome():
    configs_file = Path(NamedTemporaryFile(suffix=".dconf").name)
    configs_file.write_text(gnome_configs)
    with configs_file.open() as file:
        subprocess.run(["dconf", "load", "/"], stdin=file, check=True)


def download_font(url: str) -> None:
    """Download a font into the fonts' directory."""
    file_path = urlparse(url).path
    font_file = FONTS / Path(file_path).name
    if font_file.exists():
        return
    response = requests.get(url)
    font_file.write_bytes(response.content)


def download_fonts(url: str, ttf_paths: list = []) -> None:
    """Download all or selected font files from an archive into the fonts' directory"""
    if all((FONTS / Path(ttf_path).name).exists() for ttf_path in ttf_paths):
        return

    response = requests.get(url)
    FONTS.mkdir(parents=True, exist_ok=True)

    with ZipFile(io.BytesIO(response.content)) as zip_file:
        if not ttf_paths:
            ttf_paths = zip_file.filelist
        for ttf_path in ttf_paths:
            font_file = FONTS / Path(ttf_path).name
            with zip_file.open(ttf_path) as font:
                font_file.write_bytes(font.read())


def build_font_cache() -> None:
    """Install the fonts"""
    command = ["sudo", "fc-cache", "-f"]
    subprocess.run(command)


def main():
    FONTS.mkdir(parents=True, exist_ok=True)
    # JetBrains Fonts
    initial = list(FONTS.iterdir())

    url = "https://download.jetbrains.com/fonts/JetBrainsMono-2.304.zip"
    file_paths = [
        "fonts/ttf/JetBrainsMono-Regular.ttf",
        "fonts/ttf/JetBrainsMono-Bold.ttf",
        "fonts/ttf/JetBrainsMono-Italic.ttf",
        "fonts/ttf/JetBrainsMono-BoldItalic.ttf",
    ]
    download_fonts(url, file_paths)

    # Meslo Nerd Fonts
    url_template = (
        "https://github.com/ryanoasis/nerd-fonts/raw/master/patched-fonts/"
        "Meslo/S/{}/MesloLGSNerdFontMono-{}.ttf"
    )
    for style in "Regular", "Bold", "Italic", "BoldItalic":
        url = url_template.format(style, style)
        download_font(url)

    final = list(FONTS.iterdir())

    if initial != final:
        build_font_cache()

    configure_gnome()


if __name__ == "__main__":
    main()
