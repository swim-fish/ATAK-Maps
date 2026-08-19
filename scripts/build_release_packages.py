#!/usr/bin/env python3
"""Build the complete and Taiwan-tested release ZIP archives."""

import argparse
import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from mapvalidator.catalog import (  # noqa: E402
    PACKAGE_NAME,
    PACKAGE_UID,
    TAIWAN_ESSENTIAL_PACKAGE_NAME,
    TAIWAN_ESSENTIAL_PACKAGE_UID,
    TAIWAN_PACKAGE_NAME,
    TAIWAN_PACKAGE_UID,
    iter_map_files,
)
from mapvalidator.data_package import build_data_package  # noqa: E402
from mapvalidator.package_profiles import (  # noqa: E402
    select_listed_profile_map_files,
    select_profile_map_files,
)

TAIWAN_PROFILE = REPO_ROOT / "map-tests" / "taiwan-taichung.json"
TAIWAN_ESSENTIAL_PROFILE = (
    REPO_ROOT / "package-profiles" / "taiwan-essential.json"
)


def write_checksums(package_paths: list[Path], output_path: Path) -> None:
    """Write GNU-compatible SHA-256 checksums for release assets."""
    lines = [
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}"
        for path in package_paths
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "dist",
        help="Output directory (default: dist)",
    )
    args = parser.parse_args()

    all_maps = iter_map_files(REPO_ROOT)
    taiwan_maps = select_profile_map_files(all_maps, REPO_ROOT, TAIWAN_PROFILE)
    taiwan_essential_maps = select_listed_profile_map_files(
        all_maps, REPO_ROOT, TAIWAN_ESSENTIAL_PROFILE
    )
    all_package = args.output_dir / "atak-maps.zip"
    taiwan_package = args.output_dir / "atak-maps-taiwan.zip"
    taiwan_essential_package = (
        args.output_dir / "atak-maps-taiwan-essential.zip"
    )
    build_data_package(
        all_maps,
        REPO_ROOT,
        all_package,
        package_uid=PACKAGE_UID,
        package_name=PACKAGE_NAME,
    )
    build_data_package(
        taiwan_maps,
        REPO_ROOT,
        taiwan_package,
        package_uid=TAIWAN_PACKAGE_UID,
        package_name=TAIWAN_PACKAGE_NAME,
    )
    build_data_package(
        taiwan_essential_maps,
        REPO_ROOT,
        taiwan_essential_package,
        package_uid=TAIWAN_ESSENTIAL_PACKAGE_UID,
        package_name=TAIWAN_ESSENTIAL_PACKAGE_NAME,
    )
    write_checksums(
        [all_package, taiwan_package, taiwan_essential_package],
        args.output_dir / "SHA256SUMS",
    )
    print(
        f"Built ATAK Data Packages: all={len(all_maps)}, "
        f"Taiwan-tested={len(taiwan_maps)}, "
        f"Taiwan-essential={len(taiwan_essential_maps)}."
    )


if __name__ == "__main__":
    main()
