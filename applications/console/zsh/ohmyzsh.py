import os
import re
import subprocess

from config import HOME

ZSHRC = HOME / ".zshrc"


def install_ohmyzsh():
    if (HOME / ".oh-my-zsh").exists():
        return
    script = '"$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"'
    command = f"sh -c {script} -- --unattended --skip-chsh"
    subprocess.run(command, shell=True)


def set_theme(theme: str):
    zshrc = ZSHRC.read_text()

    pattern = r'^ZSH_THEME=".*"$'
    repl = f'ZSH_THEME="{theme}"'

    zshrc = re.sub(pattern, repl, zshrc, flags=re.MULTILINE)
    ZSHRC.write_text(zshrc)


def get_plugins() -> list:
    zshrc = ZSHRC.read_text()

    pattern = r"^plugins=\((.*?)\)$"
    match = re.search(pattern, zshrc, re.MULTILINE)

    if not match:
        return []

    return match.group(1).split()


def set_plugins(plugins: list) -> None:
    zshrc = ZSHRC.read_text()

    pattern = r"^plugins=\((.*?)\)$"
    repl = "plugins=(" + " ".join(plugins) + ")"

    zshrc = re.sub(pattern, repl, zshrc, flags=re.MULTILINE)
    ZSHRC.write_text(zshrc)


def add_plugin(plugin: str):
    plugins = get_plugins()
    if plugin not in plugins:
        plugins.append(plugin)
        set_plugins(plugins)


def remove_plugin(plugin: str):
    plugins = get_plugins()
    if plugin in plugins:
        plugins.remove(plugin)
        set_plugins(plugins)


def add_config(config: str, heading="User configuration"):
    zshrc = ZSHRC.read_text()

    pattern = rf"(^# {heading}$.*?\n)\n^# "
    match = re.search(pattern, zshrc, re.MULTILINE | re.DOTALL)

    if match and (config not in match.group(1)):
        configs = match.group(1)
        zshrc = zshrc.replace(configs, f"{configs}\n{config}")
        ZSHRC.write_text(zshrc)


def add_env(key: str, value: str, export=True):
    config = f'{key}="{value}"\n'
    if export:
        config = "export " + config

    add_config(config)


def add_alias(alias: str, command: str):
    config = f'alias {alias}="{command}"\n'
    add_config(config, heading="Example aliases")


def change_shell():
    if not os.getenv("SHELL").endswith("zsh"):
        command = ["chsh", "-s", "/usr/bin/zsh"]
        subprocess.run(command, check=True)


def fix_prompt_reset():
    config = """reset-prompt() {
  local precmd
  for precmd in $precmd_functions; do
    $precmd
  done
  zle .reset-prompt
}
zle -N reset-prompt reset-prompt

clear-screen() {
  local precmd
  for precmd in $precmd_functions; do
    $precmd
  done
  zle .clear-screen
}
zle -N clear-screen clear-screen

bindkey '^R' reset-prompt
"""
    add_config(config)
