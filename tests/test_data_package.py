import xml.etree.ElementTree as ET
import zipfile

import pytest

from mapvalidator.data_package import (
    DataPackageValidationError,
    build_data_package,
    validate_data_package,
)


def _write_map(root, relative_path):
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "<?xml version=\"1.0\"?><customMapSource>"
        "<name>Test</name><maxZoom>1</maxZoom>"
        "<url>https://example.test/{$z}/{$x}/{$y}</url>"
        "</customMapSource>",
        encoding="utf-8",
    )
    return path


def test_build_data_package_authors_atak_manifest_v2(tmp_path):
    first = _write_map(tmp_path, "Google/first.xml")
    second = _write_map(tmp_path, "TaiwanMaps/second.xml")
    output = tmp_path / "maps.zip"

    build_data_package(
        [second, first],
        tmp_path,
        output,
        package_uid="package-uid",
        package_name="Taiwan Maps",
    )

    with zipfile.ZipFile(output) as archive:
        assert archive.namelist() == [
            "MANIFEST/manifest.xml",
            "content/Google/first.xml",
            "content/TaiwanMaps/second.xml",
        ]
        manifest = ET.fromstring(archive.read("MANIFEST/manifest.xml"))

    assert manifest.tag == "MissionPackageManifest"
    assert manifest.get("version") == "2"
    configuration = manifest.find("Configuration")
    identity = {
        parameter.get("name"): parameter.get("value")
        for parameter in configuration.findall("Parameter")
    }
    assert identity == {"uid": "package-uid", "name": "Taiwan Maps"}
    contents = manifest.find("Contents").findall("Content")
    assert [content.get("zipEntry") for content in contents] == [
        "content/Google/first.xml",
        "content/TaiwanMaps/second.xml",
    ]
    assert all(
        content.find("Parameter").attrib
        == {"name": "contentType", "value": "External Native Data"}
        for content in contents
    )

    second_output = tmp_path / "maps-second.zip"
    build_data_package(
        [first, second],
        tmp_path,
        second_output,
        package_uid="package-uid",
        package_name="Taiwan Maps",
    )
    assert output.read_bytes() == second_output.read_bytes()


def test_validate_data_package_rejects_plain_zip(tmp_path):
    output = tmp_path / "plain.zip"
    with zipfile.ZipFile(output, "w") as archive:
        archive.writestr("content/map.xml", "<customMapSource/>")

    with pytest.raises(DataPackageValidationError, match="exactly one"):
        validate_data_package(output)


def test_validate_data_package_rejects_missing_content_type(tmp_path):
    output = tmp_path / "missing-content-type.zip"
    manifest = """<?xml version="1.0" encoding="UTF-8"?>
<MissionPackageManifest version="2">
  <Configuration>
    <Parameter name="uid" value="uid"/>
    <Parameter name="name" value="name"/>
  </Configuration>
  <Contents><Content zipEntry="content/map.xml"/></Contents>
</MissionPackageManifest>
"""
    with zipfile.ZipFile(output, "w") as archive:
        archive.writestr("MANIFEST/manifest.xml", manifest)
        archive.writestr("content/map.xml", "<customMapSource/>")

    with pytest.raises(DataPackageValidationError, match="contentType"):
        validate_data_package(output)


def test_validate_data_package_rejects_unsafe_archive_path(tmp_path):
    output = tmp_path / "unsafe.zip"
    with zipfile.ZipFile(output, "w") as archive:
        archive.writestr("MANIFEST/manifest.xml", "<invalid/>")
        archive.writestr("../map.xml", "<customMapSource/>")

    with pytest.raises(DataPackageValidationError, match="Unsafe archive path"):
        validate_data_package(output)
