#!/usr/bin/env python3
"""Generate docs/maps.md and docs/qr/*.png from the repo's map sources."""

import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# The repo root (containing the mapvalidator package) isn't on sys.path when
# this file is invoked directly as `python scripts/gen_pages_catalog.py`
# (Python only puts the script's own directory there), so add it explicitly.
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from mapvalidator.catalog import (  # noqa: E402
    PACKAGE_FILENAME,
    PACKAGE_NAME,
    PACKAGE_SUBDIR,
    PACKAGE_UID,
    SOURCES_SUBDIR,
    TAIWAN_ESSENTIAL_PACKAGE_FILENAME,
    TAIWAN_ESSENTIAL_PACKAGE_NAME,
    TAIWAN_ESSENTIAL_PACKAGE_UID,
    TAIWAN_PACKAGE_FILENAME,
    TAIWAN_PACKAGE_NAME,
    TAIWAN_PACKAGE_UID,
    build_map_entry,
    iter_map_files,
    package_import_uri,
    render_maps_page,
    taiwan_essential_package_import_uri,
    taiwan_package_import_uri,
)
from mapvalidator.data_package import build_data_package  # noqa: E402
from mapvalidator.package_profiles import (  # noqa: E402
    select_listed_profile_map_files,
    select_profile_map_files,
)

DOCS = REPO_ROOT / "docs"
QR_DIR = DOCS / "qr"
SOURCES_DIR = DOCS / SOURCES_SUBDIR
PACKAGE_DIR = DOCS / PACKAGE_SUBDIR
DESCRIPTIONS_FILE = REPO_ROOT / "descriptions.yml"
TAIWAN_PROFILE_FILE = REPO_ROOT / "map-tests" / "taiwan-taichung.json"
TAIWAN_ESSENTIAL_PROFILE_FILE = (
    REPO_ROOT / "package-profiles" / "taiwan-essential.json"
)
# The Maps page renders at /maps/ (pretty URLs); assets live one level up.
ALL_MAPS_QR = "../qr/_all-maps.png"


def write_qr(data: str, out_path: Path) -> None:
    """Write a QR PNG encoding ``data`` (lazy import keeps the module importable)."""
    import qrcode

    out_path.parent.mkdir(parents=True, exist_ok=True)
    qrcode.make(data).save(out_path)


def load_descriptions() -> dict:
    """Load descriptions.yml (slug -> {category, text}); {} if absent."""
    if not DESCRIPTIONS_FILE.exists():
        return {}
    import yaml

    return yaml.safe_load(DESCRIPTIONS_FILE.read_text()) or {}


def main() -> None:
    map_files = iter_map_files(REPO_ROOT)
    taiwan_map_files = select_profile_map_files(
        map_files, REPO_ROOT, TAIWAN_PROFILE_FILE
    )
    taiwan_essential_map_files = select_listed_profile_map_files(
        map_files, REPO_ROOT, TAIWAN_ESSENTIAL_PROFILE_FILE
    )
    entries = [build_map_entry(f, REPO_ROOT) for f in map_files]
    for e in entries:
        write_qr(e["import_uri"], QR_DIR / f"{e['slug']}.png")
    # Publish a copy of each source XML on the site so ATAK fetches it with an
    # application/xml content type (raw githubusercontent serves text/plain,
    # which breaks ATAK's import — see mapvalidator.catalog.PAGES_BASE).
    for f in map_files:
        dest = SOURCES_DIR / f.relative_to(REPO_ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(f, dest)
    build_data_package(
        map_files,
        REPO_ROOT,
        PACKAGE_DIR / PACKAGE_FILENAME,
        package_uid=PACKAGE_UID,
        package_name=PACKAGE_NAME,
    )
    build_data_package(
        taiwan_map_files,
        REPO_ROOT,
        PACKAGE_DIR / TAIWAN_PACKAGE_FILENAME,
        package_uid=TAIWAN_PACKAGE_UID,
        package_name=TAIWAN_PACKAGE_NAME,
    )
    build_data_package(
        taiwan_essential_map_files,
        REPO_ROOT,
        PACKAGE_DIR / TAIWAN_ESSENTIAL_PACKAGE_FILENAME,
        package_uid=TAIWAN_ESSENTIAL_PACKAGE_UID,
        package_name=TAIWAN_ESSENTIAL_PACKAGE_NAME,
    )
    # QR for the whole-map-pack, shown in the Maps-page hero.
    write_qr(package_import_uri(), QR_DIR / "_all-maps.png")
    write_qr(taiwan_package_import_uri(), QR_DIR / "_taiwan-maps.png")
    write_qr(
        taiwan_essential_package_import_uri(),
        QR_DIR / "_taiwan-essential-maps.png",
    )
    descriptions = load_descriptions()
    missing = [e["slug"] for e in entries if not descriptions.get(e["slug"])]
    if missing:
        print(f"WARNING: {len(missing)} maps without a description: {missing}")
    (DOCS / "maps.md").write_text(
        render_maps_page(
            entries,
            descriptions=descriptions,
            package_uri=package_import_uri(),
            package_qr=ALL_MAPS_QR,
        )
    )
    print(
        f"Generated {len(entries)} map entries + QR codes + hosted sources + "
        f"data packages ({len(taiwan_map_files)} Taiwan-tested, "
        f"{len(taiwan_essential_map_files)} Taiwan-essential) into docs/."
    )


if __name__ == "__main__":
    main()
