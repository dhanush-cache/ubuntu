import tomllib
from pathlib import Path
from urllib.parse import urlparse

import requests
import tomli_w

from config import HOME
from installers.apt import APTInstaller

config_dir = HOME / ".config" / "alacritty"
config_dir.mkdir(parents=True, exist_ok=True)

config_file = config_dir / "alacritty.toml"


def read_configs():
    return tomllib.loads(config_file.read_text())


def write_configs(configs):
    config_file.write_text(tomli_w.dumps(configs))


def configure():
    if config_file.exists():
        return
    configs = {
        "font": {
            "size": 18.0,
            "normal": {"family": "MesloLGS Nerd Font Mono", "style": "Regular"},
            "bold": {"family": "MesloLGS Nerd Font Mono", "style": "Bold"},
            "italic": {"family": "MesloLGS Nerd Font Mono", "style": "Italic"},
        },
        "window": {"startup_mode": "Maximized"},
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
    APTInstaller("alacritty")
    configure()
    theme = "https://github.com/catppuccin/alacritty/raw/main/catppuccin-mocha.toml"
    add_config_module(theme)


if __name__ == "__main__":
    main()
