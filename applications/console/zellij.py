import subprocess
import tarfile
from tempfile import NamedTemporaryFile, TemporaryDirectory

import requests


def install_zellij():
    url = "https://github.com/zellij-org/zellij/releases/latest/download/zellij-x86_64-unknown-linux-musl.tar.gz"
    response = requests.get(url)
    archive = NamedTemporaryFile(suffix=".tar.gz")
    archive.write(response.content)
    with tarfile.open(archive.name, "r:gz") as tar:
        target = TemporaryDirectory(delete=False)
        tar.extractall(target.name)
    command = ["sudo", "mv", f"{target.name}/zellij", "/usr/local/bin"]
    subprocess.run(command)


def uninstall_zellij():
    command = ["sudo", "rm", "-rf", "/usr/local/bin/zellij"]
    subprocess.run(command)


if __name__ == "__main__":
    uninstall_zellij()
    install_zellij()
