"""Select map XML files from an explicit, test-backed package profile."""

import json
from pathlib import Path


def load_package_profile(profile_path: Path) -> dict:
    """Load and minimally validate a JSON package profile."""
    data = json.loads(profile_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "sources" not in data:
        raise ValueError(f"Invalid package profile: {profile_path}")
    return data


def select_profile_map_files(
    map_files: list[Path], root: Path, profile_path: Path
) -> list[Path]:
    """Return explicitly included files and reject stale/incomplete profiles.

    Every current map XML must have a profile entry, and every profile entry
    must point to a current map XML. This prevents newly added or renamed maps
    from silently entering or disappearing from a regional package.
    """
    profile = load_package_profile(profile_path)
    source_settings = profile["sources"]
    if not isinstance(source_settings, dict):
        raise ValueError(f"Profile sources must be a mapping: {profile_path}")
    by_relative_path = {
        path.relative_to(root).as_posix(): path for path in map_files
    }
    map_paths = set(by_relative_path)
    profile_paths = set(source_settings)

    missing = sorted(map_paths - profile_paths)
    stale = sorted(profile_paths - map_paths)
    if missing or stale:
        details = []
        if missing:
            details.append("missing entries: " + ", ".join(missing))
        if stale:
            details.append("stale entries: " + ", ".join(stale))
        raise ValueError(
            "Package profile does not match map corpus ("
            + "; ".join(details)
            + ")"
        )

    selected = []
    for relative_path in sorted(map_paths):
        include = source_settings[relative_path].get("include_in_taiwan_package")
        if not isinstance(include, bool):
            raise ValueError(
                f"Profile entry {relative_path} must define "
                "include_in_taiwan_package as a boolean"
            )
        if include:
            selected.append(by_relative_path[relative_path])
    return selected


def select_listed_profile_map_files(
    map_files: list[Path], root: Path, profile_path: Path
) -> list[Path]:
    """Return files explicitly listed by a curated package profile."""
    profile = load_package_profile(profile_path)
    listed_sources = profile["sources"]
    if not isinstance(listed_sources, list) or not all(
        isinstance(path, str) and path for path in listed_sources
    ):
        raise ValueError(f"Profile sources must be a list of paths: {profile_path}")
    if len({path.lower() for path in listed_sources}) != len(listed_sources):
        raise ValueError("Curated package profile contains duplicate paths")

    by_relative_path = {
        path.relative_to(root).as_posix(): path for path in map_files
    }
    stale = sorted(set(listed_sources) - set(by_relative_path))
    if stale:
        raise ValueError("Curated profile contains stale paths: " + ", ".join(stale))
    return [by_relative_path[path] for path in listed_sources]
