"""Apache Maven Version Selection"""

import re
from collections.abc import Iterable

_GA_VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")


def select_latest_ga(
    versions: Iterable[str], major: int | None = None, minor: int | None = None
) -> str | None:
    """Select Apache Maven Version"""
    if minor is not None and major is None:
        raise ValueError("Minor Requires Major")

    latest: tuple[int, int, int] | None = None
    selected: str | None = None

    for version in versions:
        match = _GA_VERSION.fullmatch(version)
        if match is None:
            continue

        try:
            numbers = (int(match[1]), int(match[2]), int(match[3]))

        except ValueError:
            continue

        if major is not None and numbers[0] != major:
            continue

        if minor is not None and numbers[1] != minor:
            continue

        if latest is None or numbers > latest:
            latest = numbers
            selected = version

    return selected
