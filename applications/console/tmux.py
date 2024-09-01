import subprocess

import requests

from config import HOME
from installers.apt import APTInstaller
from utils import git

configs_file = HOME / ".config" / "tmux" / "tmux.conf"


def main():
    APTInstaller("tmux")
    url = "https://github.com/tmux-plugins/tpm"
    tpm_dir = HOME / ".tmux" / "plugins" / "tpm"
    git.clone(url, tpm_dir, shallow=True)

    if not configs_file.exists():
        url = "https://raw.githubusercontent.com/dreamsofcode-io/tmux/main/tmux.conf"
        response = requests.get(url)
        configs_file.parent.mkdir(parents=True, exist_ok=True)
        configs_file.write_text(response.text)

        script = tpm_dir / "scripts" / "install_plugins.sh"
        subprocess.run([str(script)], capture_output=True)


if __name__ == "__main__":
    main()
