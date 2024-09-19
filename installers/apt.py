"""Module to work with apt packages."""

from tempfile import NamedTemporaryFile

import requests

from installers.installer import Installer


class APTInstaller(Installer):

    def __init__(self, *packages, force: bool = False) -> None:
        if not self.check(*packages):
            self.update()
            self.upgrade()
        super().__init__(*packages, force=force)

    def is_installed(self, package: str) -> bool:
        """Check if a package is installed."""
        result = self._run(["dpkg", "-s", package])
        return result.returncode == 0

    def exists(self, package: str) -> bool:
        """Check if a package is installed."""
        result = self._run(["sudo", "apt", "show", package])
        return result.returncode == 0

    def install(self, package: str) -> None:
        """Install a package."""
        self._run_with_check(["sudo", "apt", "install", "-y", package])
        print(f"Package {package} installed successfully.")

    def uninstall(self, package: str) -> None:
        """Uninstall a package."""
        self._run_with_check(["sudo", "apt", "remove", "-y", package])
        print(f"Package {package} uninstalled successfully.")

    def update(self) -> None:
        """Update the package list."""
        self._run_with_check(["sudo", "apt", "update"])
        print("Package list updated successfully.")

    def upgrade(self) -> None:
        """Upgrade all installed packages."""
        self._run_with_check(["sudo", "apt", "upgrade", "-y"])
        print("All packages upgraded successfully.")

    @staticmethod
    def install_deb(package_name: str, url: str, params: dict = None) -> None:
        """Install a .deb file from a url."""
        if APTInstaller().is_installed(package_name):
            return
        if params is None:
            params = {}
        file = NamedTemporaryFile(suffix=".deb")
        with requests.get(url, params=params, stream=True) as response:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        APTInstaller().install(file.name)
        APTInstaller().update()
