import py2exe


def main():
    py2exe.freeze(console=["patcher.py"])


if __name__ == "__main__":
    main()
