import subprocess
import tomllib
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlparse

import requests
import tomli_w

from config import HOME
from installers.apt import APTInstaller
from utils import git

config_dir = HOME / ".config" / "alacritty"
config_dir.mkdir(parents=True, exist_ok=True)

config_file = config_dir / "alacritty.toml"


def install_rust():
    if (HOME / ".cargo").exists():
        return
    command = "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y"
    subprocess.run(command, shell=True)


def uninstall_rust():
    if not (HOME / ".cargo" / "bin" / "rustup").exists():
        return
    command = "rustup self uninstall -y"
    subprocess.run(command, shell=True)


def install_alacritty():
    if Path("/usr/local/bin/alacritty").exists():
        return
    dependencies = (
        "cmake",
        "pkg-config",
        "libfreetype-dev",
        "libfontconfig1-dev",
        "libxcb-xfixes0-dev",
        "libxkbcommon-dev",
        "python3",
    )

    target = TemporaryDirectory(delete=False)
    source_code = Path(target.name) / "alacritty"
    git.clone("https://github.com/alacritty/alacritty.git", source_code, shallow=True)
    command = "~/.cargo/bin/cargo build --release --no-default-features --features=x11"
    try:
        APTInstaller(*dependencies)
        install_rust()
        subprocess.run(command, cwd=source_code, shell=True)
    finally:
        uninstall_rust()
        for pkg in dependencies:
            if pkg.startswith("lib"):
                APTInstaller().uninstall(pkg)

    commands = (
        "sudo cp target/release/alacritty /usr/local/bin",
        "sudo cp extra/logo/alacritty-term.svg /usr/share/pixmaps/Alacritty.svg",
        "sudo desktop-file-install extra/linux/Alacritty.desktop",
        "sudo update-desktop-database",
        "sudo update-alternatives --install /usr/bin/x-terminal-emulator x-terminal-emulator /usr/local/bin/alacritty 50",
    )
    for command in commands:
        subprocess.run(command, cwd=source_code, shell=True)


def read_configs():
    return tomllib.loads(config_file.read_text())


def write_configs(configs):
    config_file.write_text(tomli_w.dumps(configs))


def configure():
    if config_file.exists():
        return
    configs = {
        "font": {
            "size": 16.0,
            "normal": {"family": "MesloLGS Nerd Font Mono", "style": "Regular"},
            "bold": {"family": "MesloLGS Nerd Font Mono", "style": "Bold"},
            "italic": {"family": "MesloLGS Nerd Font Mono", "style": "Italic"},
        },
        "window": {"dimensions": {"lines": 30, "columns": 100}},
    }
    write_configs(configs)


def add_config_module(url: str):
    file_path = urlparse(url).path
    module = config_dir / Path(file_path).name
    if module.exists():
        return

    response = requests.get(url)
    module.write_text(response.text)

    configs = read_configs()

    imports = set(configs.get("import", []))
    import_value = f"~/{module.relative_to(HOME)}"
    imports.add(import_value)
    configs["import"] = list(imports)

    write_configs(configs)


def main():
    install_alacritty()
    configure()
    theme = "https://github.com/catppuccin/alacritty/raw/main/catppuccin-mocha.toml"
    add_config_module(theme)


if __name__ == "__main__":
    main()
