import requests
from bs4 import BeautifulSoup

from installers.apt import APTInstaller


def __get_url_1():
    url = "https://netbeans.apache.org/front/main/download"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    tag = soup.select_one("a.xref.page.button.success")
    return f"{url}/{tag["href"]}"


def __get_url_2():
    url = __get_url_1()
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    tags = soup.select("div.ulist > ul > li > p > a")
    return next(tag["href"] for tag in tags if tag["href"].endswith(".deb"))


def get_download_url():
    url = __get_url_2()
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    tags = soup.select("main#maincontent > div.container > p > a")
    return next(tag["href"] for tag in tags if tag["href"].endswith(".deb"))


def install_netbeans():
    url = get_download_url()
    APTInstaller.install_deb("apache-netbeans", url)


if __name__ == "__main__":
    install_netbeans()
