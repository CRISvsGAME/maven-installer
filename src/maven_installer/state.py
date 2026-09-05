"""Maven Installer State"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast

SCHEMA_VERSION = 1
EXPECTED_FIELDS = {"schema_version", "active_version", "installed_versions"}


class StateException(Exception):
    """State Exception."""


@dataclass(frozen=True)
class State:
    """State"""

    schema_version: int
    active_version: str
    installed_versions: tuple[str, ...]


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    data: dict[str, object] = {}

    for key, value in pairs:
        if key in data:
            raise StateException(f"Duplicate State Field: {key}")

        data[key] = value

    return data


def load_state(path: Path) -> State | None:
    """Load State"""
    try:
        with path.open("r", encoding="utf-8") as file:
            raw_data = json.load(file, object_pairs_hook=_unique_object)

    except FileNotFoundError:
        return None

    except json.JSONDecodeError as e:
        raise StateException(f"Invalid State Format: {e}") from e

    except UnicodeError as e:
        raise StateException(f"Invalid State Encoding: {e}") from e

    except OSError as e:
        raise StateException(f"Unreadable State File: {e}") from e

    if not isinstance(raw_data, dict):
        raise StateException(f"Invalid State Type: {raw_data!r}")

    data = cast(dict[str, object], raw_data)

    if set(data) != EXPECTED_FIELDS:
        raise StateException("Invalid State Fields")

    schema_version = data["schema_version"]
    active_version = data["active_version"]
    installed_versions = data["installed_versions"]

    if (
        not isinstance(schema_version, int)
        or isinstance(schema_version, bool)
        or schema_version != SCHEMA_VERSION
    ):
        raise StateException(f"Unsupported Schema Version: {schema_version!r}")

    if not isinstance(active_version, str) or not active_version.strip():
        raise StateException(f"Unsupported Active Version: {active_version!r}")

    if not isinstance(installed_versions, list) or not installed_versions:
        raise StateException(f"Unsupported Installed Versions: {installed_versions!r}")

    versions = cast(list[object], installed_versions)

    if any(not isinstance(version, str) or not version.strip() for version in versions):
        raise StateException(f"Unsupported Installed Versions: {installed_versions!r}")

    valid_versions = cast(list[str], versions)
    unique_versions = set(valid_versions)

    if len(valid_versions) != len(unique_versions):
        raise StateException("Duplicate Installed Versions")

    if active_version not in unique_versions:
        raise StateException("Uninstalled Active Version")

    return State(
        schema_version=schema_version,
        active_version=active_version,
        installed_versions=tuple(valid_versions),
    )
