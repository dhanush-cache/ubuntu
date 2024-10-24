from applications.console.fzf import install_fzf
from applications.console.zellij import install_zellij
from applications.console.zsh import p10k, ohmyzsh
from config import HOME
from installers.apt import APTInstaller
from utils import git, environment


def main():
    APTInstaller("zsh", "curl", "git")

    ohmyzsh.install_ohmyzsh()
    ohmyzsh.change_shell()
    ohmyzsh.fix_prompt_reset()

    url = "https://github.com/romkatv/powerlevel10k.git"
    path = HOME / ".oh-my-zsh" / "custom" / "themes" / "powerlevel10k"
    git.clone(url, path, shallow=True)
    ohmyzsh.set_theme("powerlevel10k/powerlevel10k")
    p10k.configure_p10k()

    url = "https://github.com/zsh-users/zsh-autosuggestions"
    path = HOME / ".oh-my-zsh" / "custom" / "plugins" / "zsh-autosuggestions"
    git.clone(url, path, shallow=True)
    ohmyzsh.add_plugin("zsh-autosuggestions")

    url = "https://github.com/zsh-users/zsh-syntax-highlighting.git"
    path = HOME / ".oh-my-zsh" / "custom" / "plugins" / "zsh-syntax-highlighting"
    git.clone(url, path, shallow=True)
    ohmyzsh.add_plugin("zsh-syntax-highlighting")

    path = HOME / ".local" / "bin"
    environment.add_path(path)

    install_zellij()
    install_fzf()
    APTInstaller("tree", "stow")


if __name__ == "__main__":
    main()
