from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup

from installers.apt import APTInstaller


def get_file_id(url: str, params: dict = None) -> int:
    if params is None:
        params = {}
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")
    tag = soup.find("a", string="Download")
    return int(parse_qs(urlparse(tag["href"]).query)["id"][0])


def get_download_url(file_id: int) -> str:
    url = "https://dev.mysql.com/downloads/file"
    params = {"id": file_id}
    text = "No thanks, just start my download."
    response = requests.get(url, params=params)

    soup = BeautifulSoup(response.text, "html.parser")
    tag = soup.find("a", string=text)

    return f"https://dev.mysql.com{tag["href"]}"


def get_apt_config_url() -> str:
    url = "https://dev.mysql.com/downloads/repo/apt/"
    file_id = get_file_id(url)
    return get_download_url(file_id)


def get_workbench_url() -> str:
    url = "https://dev.mysql.com/downloads/workbench/"
    params = {"tpl": "platform", "os": 22}
    file_id = get_file_id(url, params)
    return get_download_url(file_id)


def main():
    package_name = "mysql-apt-config"
    if not APTInstaller().is_installed(package_name):
        url = get_apt_config_url()
        APTInstaller.install_deb(package_name, url)

    package_name = "mysql-workbench-community"
    if not APTInstaller().is_installed(package_name):
        url = get_workbench_url()
        APTInstaller.install_deb(package_name, url)

    APTInstaller("mysql-server")


if __name__ == "__main__":
    main()
