import subprocess
from abc import ABC, abstractmethod


class UnresolvedDependenciesError(Exception):
    pass


class Installer(ABC):

    def __init__(self, *packages, force: bool = False) -> None:
        if not packages:
            return
        self.resolve(*packages, force=force)
        if not self.check(*packages):
            raise UnresolvedDependenciesError(
                "Dependencies were not resolved successfully!"
            )

    @staticmethod
    def _run(command: list) -> subprocess.CompletedProcess:
        return subprocess.run(command, capture_output=True, text=True, check=False)

    @staticmethod
    def _run_with_check(command: list) -> None:
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as ex:
            print(f"Error: {ex}")

    @abstractmethod
    def is_installed(self, package: str) -> bool:
        pass

    @abstractmethod
    def install(self, package: str) -> None:
        pass

    @abstractmethod
    def uninstall(self, package: str) -> None:
        pass

    def resolve(self, *packages, force: bool = False) -> None:
        for package in packages:
            if force or not self.is_installed(package):
                self.install(package)

    def check(self, *packages) -> bool:
        for package in packages:
            if not self.is_installed(package):
                return False
        return True
