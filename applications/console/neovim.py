import subprocess
import tarfile
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

import requests

from applications.console.zsh import ohmyzsh
from config import HOME
from installers.apt import APTInstaller
from utils import git

binary = Path("/opt/nvim-linux64/bin/nvim")


def install_neovim():
    if binary.exists():
        return
    url = (
        "https://github.com/neovim/neovim/releases/latest/download/nvim-linux64.tar.gz"
    )
    archive = NamedTemporaryFile(suffix=".tar.gz")
    response = requests.get(url)
    archive.write(response.content)

    with tarfile.open(archive.name, "r:gz") as tar:
        target = TemporaryDirectory(delete=False)
        tar.extractall(target.name)
    src = Path(target.name) / "nvim-linux64"
    target = Path(f"/opt/nvim-linux64")
    subprocess.run(["sudo", "mv", str(src), str(target)])
    path = f"$PATH:/opt/nvim-linux64/bin"
    ohmyzsh.add_env("PATH", path)


def configure_neovim():
    APTInstaller("python3", "python3-pip", "python3-venv", "npm")
    url = "https://github.com/NvChad/starter"
    path = HOME / ".config" / "nvim"
    git.clone(url, path, shallow=True)
    command = [str(binary), "--headless", "-c", "q"]
    subprocess.run(command)


def main():
    install_neovim()
    configure_neovim()


if __name__ == "__main__":
    main()
