from applications.jetbrains import install_toolbox
from applications.netbeans import install_netbeans
from installers.apt import APTInstaller
from installers.vscode import VSCodeExtension


def install_vscode():
    url = "https://code.visualstudio.com/sha/download"
    params = {"build": "stable", "os": "linux-deb-x64"}
    APTInstaller.install_deb("code", url, params)


def install_vscode_extensions():
    extensions = [
        "dracula-theme.theme-dracula",
        "PKief.material-icon-theme",
        "GitHub.github-vscode-theme",
        "esbenp.prettier-vscode",
        "EditorConfig.EditorConfig",
        "eamodio.gitlens",
        "mhutchie.git-graph",
        "ms-python.python",
        "ms-pyright.pyright",
        "ms-python.autopep8",
        "formulahendry.code-runner",
        "mkhl.shfmt",
        "timonwong.shellcheck",
        "foxundermoon.shell-format",
        "ms-vscode.cpptools",
    ]
    VSCodeExtension(*extensions)


def main():
    install_vscode()
    install_vscode_extensions()
    install_toolbox()
    install_netbeans()


if __name__ == "__main__":
    main()
