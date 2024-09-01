"""Module to work with termux packages."""

from installers.installer import Installer


class PIPInstaller(Installer):
    def is_installed(self, package: str) -> bool:
        """Check if a package is installed."""
        result = self._run(["pip", "show", package])
        return result.returncode == 0

    def install(self, package: str) -> None:
        """Install a package."""
        self._run_with_check(["pip", "install", package])

    def uninstall(self, package: str) -> None:
        """Uninstall a package."""
        self._run_with_check(["pip", "uninstall", "-y", package])
