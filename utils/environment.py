import os
from email.generator import Generator
from pathlib import Path

from config import HOME

environment = HOME / ".config" / "environment.d" / "environment.conf"


def get_paths() -> Generator:
    return (Path(path).absolute() for path in os.getenv("PATH").split(":"))


def get_envs(file=environment) -> Generator:
    if not file.exists():
        file.parent.mkdir(parents=True, exist_ok=True)
        file.touch()
    return (
        tuple(line.split("=")) for line in file.read_text().split("\n") if "=" in line
    )


def add_env(key: str, value: str, file=environment):
    if os.getenv(key) == value:
        return
    if (key, value) in get_envs(file):
        return
    with file.open("a") as target:
        target.write(f"{key}={value}\n")


def add_path(path: Path, file=environment):
    if path.absolute() in get_paths():
        return
    key = "PATH"
    value = f"${key}:{path.absolute()}"
    add_env(key, value, file)
