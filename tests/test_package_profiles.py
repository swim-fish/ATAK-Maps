import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from mapvalidator.catalog import (
    TAIWAN_ESSENTIAL_PACKAGE_FILENAME,
    TAIWAN_ESSENTIAL_PACKAGE_NAME,
    TAIWAN_ESSENTIAL_PACKAGE_UID,
    iter_map_files,
)
from mapvalidator.package_profiles import (
    load_package_profile,
    select_listed_profile_map_files,
    select_profile_map_files,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def _write_profile(tmp_path, sources):
    path = tmp_path / "profile.json"
    path.write_text(json.dumps({"sources": sources}), encoding="utf-8")
    return path


def test_load_package_profile_requires_sources_mapping(tmp_path):
    profile_path = tmp_path / "profile.json"
    profile_path.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid package profile"):
        load_package_profile(profile_path)


def test_select_profile_map_files_returns_only_explicit_includes(tmp_path):
    included = tmp_path / "A" / "included.xml"
    excluded = tmp_path / "B" / "excluded.xml"
    included.parent.mkdir()
    excluded.parent.mkdir()
    included.write_text("<map/>", encoding="utf-8")
    excluded.write_text("<map/>", encoding="utf-8")
    profile_path = _write_profile(
        tmp_path,
        {
            "A/included.xml": {"include_in_taiwan_package": True},
            "B/excluded.xml": {"include_in_taiwan_package": False},
        },
    )

    selected = select_profile_map_files(
        [excluded, included], tmp_path, profile_path
    )

    assert selected == [included]


@pytest.mark.parametrize(
    ("sources", "error"),
    [
        ({}, "missing entries"),
        (
            {
                "A/included.xml": {"include_in_taiwan_package": True},
                "B/stale.xml": {"include_in_taiwan_package": False},
            },
            "stale entries",
        ),
    ],
)
def test_select_profile_map_files_rejects_incomplete_or_stale_profile(
    tmp_path, sources, error
):
    included = tmp_path / "A" / "included.xml"
    included.parent.mkdir()
    included.write_text("<map/>", encoding="utf-8")
    profile_path = _write_profile(tmp_path, sources)

    with pytest.raises(ValueError, match=error):
        select_profile_map_files([included], tmp_path, profile_path)


def test_select_profile_map_files_requires_boolean_flag(tmp_path):
    included = tmp_path / "A" / "included.xml"
    included.parent.mkdir()
    included.write_text("<map/>", encoding="utf-8")
    profile_path = _write_profile(
        tmp_path,
        {"A/included.xml": {"include_in_taiwan_package": "yes"}},
    )

    with pytest.raises(ValueError, match="must define"):
        select_profile_map_files([included], tmp_path, profile_path)


def test_select_listed_profile_map_files_preserves_curated_order(tmp_path):
    first = tmp_path / "A" / "first.xml"
    second = tmp_path / "B" / "second.xml"
    first.parent.mkdir()
    second.parent.mkdir()
    first.write_text("<map/>", encoding="utf-8")
    second.write_text("<map/>", encoding="utf-8")
    profile_path = _write_profile(
        tmp_path,
        ["B/second.xml", "A/first.xml"],
    )

    selected = select_listed_profile_map_files(
        [first, second], tmp_path, profile_path
    )

    assert selected == [second, first]


@pytest.mark.parametrize(
    ("sources", "error"),
    [
        (["A/first.xml", "A/first.xml"], "duplicate"),
        (["A/missing.xml"], "stale paths"),
        ({"A/first.xml": {}}, "list of paths"),
    ],
)
def test_select_listed_profile_map_files_rejects_invalid_profiles(
    tmp_path, sources, error
):
    first = tmp_path / "A" / "first.xml"
    first.parent.mkdir()
    first.write_text("<map/>", encoding="utf-8")
    profile_path = _write_profile(tmp_path, sources)

    with pytest.raises(ValueError, match=error):
        select_listed_profile_map_files([first], tmp_path, profile_path)


def test_taiwan_release_profiles_only_include_confirmed_custom_map_sources():
    map_files = iter_map_files(REPO_ROOT)
    tested = select_profile_map_files(
        map_files,
        REPO_ROOT,
        REPO_ROOT / "map-tests" / "taiwan-taichung.json",
    )
    essential = select_listed_profile_map_files(
        map_files,
        REPO_ROOT,
        REPO_ROOT / "package-profiles" / "taiwan-essential.json",
    )

    assert len(tested) == 32
    assert len(essential) == 14
    assert {ET.parse(path).getroot().tag for path in tested + essential} == {
        "customMapSource"
    }

    profile = load_package_profile(
        REPO_ROOT / "package-profiles" / "taiwan-essential.json"
    )
    assert profile["package"] == {
        "filename": TAIWAN_ESSENTIAL_PACKAGE_FILENAME,
        "uid": TAIWAN_ESSENTIAL_PACKAGE_UID,
        "name": TAIWAN_ESSENTIAL_PACKAGE_NAME,
    }
