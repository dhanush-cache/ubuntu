from config import HOME

config_file = HOME / ".config" / "pip" / "pip.conf"
configs = """[global]
break-system-packages = true
user = true
"""


def main():
    config_file.parent.mkdir(parents=True, exist_ok=True)
    config_file.write_text(configs)


if __name__ == "__main__":
    main()
