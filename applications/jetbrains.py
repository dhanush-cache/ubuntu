import json
import subprocess
import tarfile
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

import requests

from config import HOME
from installers.apt import APTInstaller
from utils import environment

APTInstaller(
    "libfuse2t64",
    "libxi6",
    "libxrender1",
    "libxtst6",
    "mesa-utils",
    "libfontconfig1",
    "libgtk-3-bin",
    "tar",
    "dbus-user-session",
)


def is_installed() -> bool:
    toolbox_binary = HOME / ".local/share/JetBrains/Toolbox/bin/jetbrains-toolbox"
    return toolbox_binary.exists()


def get_toolbox_url() -> str:
    url = "https://data.services.jetbrains.com/products"
    params = {
        "code": "TBA",
        "release.type": "release",
        "fields": "releases",
    }
    response = requests.get(url, params=params)
    data = json.loads(response.text)
    return data[0]["releases"][0]["downloads"]["linux"]["link"]


def install_toolbox() -> None:
    if not is_installed():
        __install()
    scripts_path = HOME / ".local" / "share" / "JetBrains" / "Toolbox" / "scripts"
    environment.add_path(scripts_path)


def __install():
    url = get_toolbox_url()
    archive = NamedTemporaryFile(suffix=".tar.gz")
    target = TemporaryDirectory()
    response = requests.get(url)
    archive.write(response.content)
    with tarfile.open(archive.name, "r:gz") as tar:
        for file in tar.getmembers():
            if file.isfile():
                tar.extract(file, path=target.name)
    executable = next(Path(target.name).rglob("jetbrains-toolbox"))
    subprocess.run([executable], check=True)


if __name__ == "__main__":
    install_toolbox()
