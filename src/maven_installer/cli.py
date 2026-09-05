"""Maven Installer CLI"""

import argparse
import sys
from pathlib import Path
from typing import NoReturn

from maven_installer.state import StateException, load_state

STATE_PATH = Path("/var/lib/maven-installer/state.json")


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
        state = load_state(STATE_PATH)

        if state is None:
            print("No State")
            return

        print(state)

    def __help(self) -> str:
        """Help"""
        message = (
            "Usage: install-maven [-h]\n\n"
            "Options:\n"
            "    -h, --help  Show this help message and exit"
        )
        return message


def main() -> None:
    """Main"""
    try:
        CLI()
    except (CLIException, StateException) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
