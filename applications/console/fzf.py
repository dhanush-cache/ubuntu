import subprocess

from config import HOME
from utils import git


def install_fzf():
    fzf_path = HOME / ".fzf"
    if fzf_path.exists():
        return
    git.clone("https://github.com/junegunn/fzf.git", fzf_path, shallow=True)

    install_script = fzf_path / "install"
    command = [str(install_script)]
    opts = ["--key-bindings", "--completion", "--update-rc"]
    command += opts
    subprocess.run(command)


if __name__ == "__main__":
    install_fzf()
