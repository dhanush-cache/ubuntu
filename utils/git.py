"""Module to work with git commands"""

import subprocess
from pathlib import Path


def clone(url: str, path: Path = Path.home(), shallow: bool = False) -> None:
    """Clones a git repo to a specified path."""
    if path.exists():
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    command = ["git", "clone", url]
    if shallow:
        command.insert(2, "--depth=1")
    if path != Path.home():
        command.append(str(path))

    subprocess.run(command, check=True)


def config(key: str, value: str, level="global"):
    """Sets git's configurations."""
    command = ["git", "config", f"--{level}", key, value]
    subprocess.run(command)
