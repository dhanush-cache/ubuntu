import style
from applications import code_editors, mysql, firefox
from applications.console import alacritty, terminal, tmux, neovim, pip_config


def main():
    alacritty.main()
    terminal.main()
    pip_config.main()
    style.main()
    mysql.main()
    code_editors.main()
    firefox.main()
    tmux.main()
    neovim.main()


if __name__ == "__main__":
    main()
