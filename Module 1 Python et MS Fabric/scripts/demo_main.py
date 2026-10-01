"""Démonstration de l'idiome main."""
import sys


def main(argv=None) -> None:
    arguments = sys.argv[1:] if argv is None else argv
    print(f"__name__ vaut : {__name__}")
    print(f"Arguments     : {arguments}")


if __name__ == "__main__":
    main()
