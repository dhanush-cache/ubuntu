import re
import subprocess
import tarfile
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

import requests

from config import HOME


def is_installed(binary: str):
    return Path(f"/usr/local/bin/{binary}").exists()


def get_profiles():
    profiles_config = HOME / ".mozilla" / "firefox" / "profiles.ini"
    if not profiles_config.exists():
        return []
    data = profiles_config.read_text()
    pattern = r"^Name=(.*)$"
    return re.findall(pattern, data, re.MULTILINE)


def install(product: str, binary_name: str):
    if is_installed(binary_name):
        return
    url = "https://download.mozilla.org/"
    params = {"os": "linux64", "lang": "en-US", "product": product}
    response = requests.get(url, params=params)
    archive = NamedTemporaryFile(suffix=".tar.bz2")
    archive.write(response.content)
    with tarfile.open(archive.name, "r:bz2") as tar:
        target = TemporaryDirectory(delete=False)
        tar.extractall(target.name)

    src = Path(target.name) / "firefox"
    target = Path(f"/opt/{binary_name}")
    subprocess.run(["sudo", "mv", src, target], check=True)

    binary_src = target / "firefox"
    binary_link = Path(f"/usr/local/bin/{binary_name}")
    subprocess.run(["sudo", "ln", "-s", binary_src, binary_link])


def uninstall(binary_name: str):
    if not is_installed(binary_name):
        return
    binary_link = Path(f"/usr/local/bin/{binary_name}")
    target = binary_link.readlink().parent
    command = ["sudo", "rm", "-rf"]
    desktop = Path(f"/usr/local/share/applications/{binary_name}.desktop")

    paths_to_delete = [
        str(binary_link),
        str(target),
        str(desktop),
    ]
    command += paths_to_delete
    subprocess.run(command)


def create_profile(profile_name):
    if profile_name in get_profiles():
        return
    command = ["firefox", "--no-remote", "--CreateProfile", profile_name]
    subprocess.run(command)


def create_desktop_entry(name: str, binary_name: str, add_profile=False):
    profile = binary_name
    command = f"{binary_name}"
    args = f" --no-remote -P {profile}" if add_profile else ""
    command += args
    entry = f"""[Desktop Entry]
Name={name}
Exec={command}
Icon=/opt/{binary_name}/browser/chrome/icons/default/default128.png
Type=Application
Categories=Network;WebBrowser;
"""

    target = Path(f"/usr/local/share/applications/{binary_name}.desktop")
    if target.exists() and target.read_text() == entry:
        return

    subprocess.run(["sudo", "mkdir", "-p", target.parent], check=True)
    file = NamedTemporaryFile(suffix=".desktop")
    Path(file.name).write_text(entry)
    command = ["sudo", "mv", file.name, str(target)]
    subprocess.run(command)


def main():
    product = "firefox-latest-ssl"
    binary = "firefox"
    name = "Firefox"
    install(product, binary)
    # create_profile(binary)
    create_desktop_entry(name, binary)

    product = "firefox-devedition-latest-ssl"
    binary = "firefox-devedition"
    name = "Firefox Developer Edition"
    install(product, binary)
    create_profile(binary)
    create_desktop_entry(name, binary, add_profile=True)


if __name__ == "__main__":
    uninstall("firefox")
    uninstall("firefox-devedition")
    main()
