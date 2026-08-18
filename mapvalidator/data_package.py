"""Build and validate ATAK Mission Package v2 archives."""

import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from mapvalidator.catalog import build_manifest

MANIFEST_PATH = "MANIFEST/manifest.xml"
MAP_CONTENT_TYPE = "External Native Data"
MAX_MANIFEST_BYTES = 10 << 20


class DataPackageValidationError(ValueError):
    """Raised when an authored package violates the ATAK package contract."""


def package_entry_path(map_file: Path, root: Path) -> str:
    """Return the safe in-package path for a repository map XML."""
    relative_path = map_file.relative_to(root).as_posix()
    entry = f"content/{relative_path}"
    _validate_archive_path(entry)
    return entry


def build_data_package(
    map_files: list[Path],
    root: Path,
    output_path: Path,
    *,
    package_uid: str,
    package_name: str,
) -> None:
    """Write and reopen a manifest-bearing ATAK Data Package ZIP."""
    ordered_files = sorted(
        map_files, key=lambda path: path.relative_to(root).as_posix()
    )
    entries = [package_entry_path(path, root) for path in ordered_files]
    if len({entry.lower() for entry in entries}) != len(entries):
        raise DataPackageValidationError(
            "Package paths must be case-insensitively unique."
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as archive:
        _write_deterministic_entry(
            archive,
            MANIFEST_PATH,
            build_manifest(
                entries,
                package_uid=package_uid,
                package_name=package_name,
            ).encode("utf-8"),
        )
        for map_file, entry in zip(ordered_files, entries):
            _write_deterministic_entry(archive, entry, map_file.read_bytes())

    validate_data_package(output_path)


def validate_data_package(package_path: Path) -> None:
    """Validate the authored subset of the ATAK Mission Package v2 contract."""
    with zipfile.ZipFile(package_path, "r") as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        if len(names) > 10_000:
            raise DataPackageValidationError("Package contains too many entries.")
        if len({name.lower() for name in names}) != len(names):
            raise DataPackageValidationError("Package contains duplicate entry paths.")
        if names.count(MANIFEST_PATH) != 1:
            raise DataPackageValidationError(
                "Package requires exactly one MANIFEST/manifest.xml."
            )
        for info in infos:
            _validate_archive_path(info.filename)
            if info.flag_bits & 0x1:
                raise DataPackageValidationError("Encrypted entries are not supported.")
            if info.compress_type not in {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}:
                raise DataPackageValidationError("Unsupported ZIP compression method.")
        if archive.testzip() is not None:
            raise DataPackageValidationError("Package CRC validation failed.")

        manifest_bytes = archive.read(MANIFEST_PATH)
        if len(manifest_bytes) > MAX_MANIFEST_BYTES:
            raise DataPackageValidationError("Manifest exceeds the 10 MiB limit.")
        if b"<!DOCTYPE" in manifest_bytes.upper():
            raise DataPackageValidationError("Manifest DOCTYPE is forbidden.")
        try:
            manifest = ET.fromstring(manifest_bytes)
        except ET.ParseError as error:
            raise DataPackageValidationError("Manifest XML is malformed.") from error

        if manifest.tag != "MissionPackageManifest" or manifest.get("version") != "2":
            raise DataPackageValidationError(
                "Manifest root must be MissionPackageManifest version 2."
            )
        configuration = manifest.findall("Configuration")
        contents = manifest.findall("Contents")
        if len(configuration) != 1 or len(contents) != 1:
            raise DataPackageValidationError(
                "Manifest requires one Configuration and one Contents element."
            )
        _require_single_parameter(configuration[0], "uid")
        _require_single_parameter(configuration[0], "name")

        references = []
        for content in contents[0].findall("Content"):
            entry = content.get("zipEntry")
            if not entry:
                raise DataPackageValidationError("Content requires zipEntry.")
            _validate_archive_path(entry)
            references.append(entry)
            content_types = [
                parameter.get("value")
                for parameter in content.findall("Parameter")
                if parameter.get("name") == "contentType"
            ]
            if content_types != [MAP_CONTENT_TYPE]:
                raise DataPackageValidationError(
                    f"Map entry {entry} requires contentType {MAP_CONTENT_TYPE}."
                )

        if len({entry.lower() for entry in references}) != len(references):
            raise DataPackageValidationError("Manifest contains duplicate references.")
        archive_content = {name.lower() for name in names if name != MANIFEST_PATH}
        manifest_content = {entry.lower() for entry in references}
        if archive_content != manifest_content:
            raise DataPackageValidationError(
                "Manifest references and archive content do not match."
            )


def _require_single_parameter(configuration: ET.Element, name: str) -> str:
    values = [
        parameter.get("value", "")
        for parameter in configuration.findall("Parameter")
        if parameter.get("name") == name
    ]
    if len(values) != 1 or not values[0].strip():
        raise DataPackageValidationError(
            f"Manifest requires exactly one non-empty {name} parameter."
        )
    return values[0]


def _write_deterministic_entry(
    archive: zipfile.ZipFile, path: str, content: bytes
) -> None:
    info = zipfile.ZipInfo(path, date_time=(1980, 1, 1, 0, 0, 0))
    # XML map packages are small. Stored entries avoid zlib-version-dependent
    # output so Release and Pages builds are byte-for-byte reproducible.
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    archive.writestr(info, content)


def _validate_archive_path(path: str) -> None:
    if (
        not path
        or "\\" in path
        or "\x00" in path
        or path.startswith("/")
        or re.match(r"^[A-Za-z]:", path)
        or any(part in {"", ".", ".."} for part in path.split("/"))
    ):
        raise DataPackageValidationError(f"Unsafe archive path: {path!r}")
