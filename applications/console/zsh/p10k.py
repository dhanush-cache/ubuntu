import re

import requests

from config import HOME

P10K = HOME / ".p10k.zsh"
ZSHRC = HOME / ".zshrc"


def remove_comments():
    p10k = P10K.read_text()
    pattern = r"\s+#.*?$"  # Comments
    p10k = re.sub(pattern, "", p10k, flags=re.MULTILINE)

    pattern = r"^\s*#.*?\n"
    p10k = re.sub(pattern, "", p10k, flags=re.MULTILINE)

    pattern = r"^\s*?\n"
    p10k = re.sub(pattern, "", p10k, flags=re.MULTILINE)

    P10K.write_text(p10k)


def download_template():
    if P10K.exists():
        return
    url = "https://raw.githubusercontent.com/romkatv/powerlevel10k/master/config/p10k-rainbow.zsh"
    response = requests.get(url)
    p10k = response.text
    P10K.write_text(p10k)


def uncomment(head: str):
    p10k = P10K.read_text()
    p10k = p10k.replace(f"# {head}", head)
    P10K.write_text(p10k)


def set_attr(key: str, value: str):
    p10k = P10K.read_text()

    pattern = rf"typeset -g {key}=.*?$"
    repl = f"typeset -g {key}={value}"
    p10k = re.sub(pattern, repl, p10k, flags=re.MULTILINE)

    P10K.write_text(p10k)


def add_references():
    zshrc = ZSHRC.read_text()

    header = """if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi"""
    footer = """[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh"""

    if (header in zshrc) or (footer in zshrc):
        return

    zshrc = f"{header}\n\n{zshrc}\n{footer}\n"
    ZSHRC.write_text(zshrc)


def configure_p10k():
    download_template()

    uncomment("os_icon")
    uncomment("prompt_char")

    set_attr("POWERLEVEL9K_PROMPT_ADD_NEWLINE", "false")
    set_attr("POWERLEVEL9K_MULTILINE_FIRST_PROMPT_PREFIX", "")
    set_attr("POWERLEVEL9K_MULTILINE_NEWLINE_PROMPT_PREFIX", "")
    set_attr("POWERLEVEL9K_MULTILINE_LAST_PROMPT_PREFIX", "")
    set_attr("POWERLEVEL9K_MULTILINE_FIRST_PROMPT_SUFFIX", "")
    set_attr("POWERLEVEL9K_MULTILINE_NEWLINE_PROMPT_SUFFIX", "")
    set_attr("POWERLEVEL9K_MULTILINE_LAST_PROMPT_SUFFIX", "")
    set_attr("POWERLEVEL9K_MULTILINE_FIRST_PROMPT_GAP_CHAR", "'─'")
    set_attr("POWERLEVEL9K_OS_ICON_FOREGROUND", "7")
    set_attr("POWERLEVEL9K_OS_ICON_BACKGROUND", "0")
    set_attr("POWERLEVEL9K_DIR_TRUNCATE_BEFORE_MARKER", "first")
    set_attr("POWERLEVEL9K_VCS_BRANCH_ICON", r"'\\uF126 '")
    set_attr("POWERLEVEL9K_TRANSIENT_PROMPT", "always")

    add_references()
    # remove_comments()
