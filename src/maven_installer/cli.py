"""Maven Installer"""

import argparse
import sys
from typing import NoReturn


class CLIException(Exception):
    """CLI Exception"""


class CLI:
    """CLI"""

    def __init__(self) -> None:
        """Init"""
        parser = argparse.ArgumentParser(add_help=False)
        parser.error = self.__argparse_error
        parser.add_argument("-h", "--help", action="store_true", help=argparse.SUPPRESS)

        self.parser = parser
        self.args = self.parser.parse_args()

        if self.args.help:
            print(self.__help())
            return

        self.__install()

    def __argparse_error(self, message: str) -> NoReturn:
        """Argparse Error"""
        raise CLIException(f"Argparse Error: {message}")

    def __install(self) -> None:
        """Install"""
        print("Install")

    def __help(self) -> str:
        """Help"""
        message = "Help"
        return message


def main() -> None:
    """Main"""
    try:
        CLI()
    except CLIException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
