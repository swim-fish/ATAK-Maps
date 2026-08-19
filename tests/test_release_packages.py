import hashlib

from scripts.build_release_packages import write_checksums


def test_write_checksums_uses_release_filenames_and_sha256(tmp_path):
    first = tmp_path / "atak-maps.zip"
    second = tmp_path / "atak-maps-taiwan.zip"
    first.write_bytes(b"all maps")
    second.write_bytes(b"taiwan maps")
    output = tmp_path / "SHA256SUMS"

    write_checksums([first, second], output)

    assert output.read_text(encoding="utf-8").splitlines() == [
        f"{hashlib.sha256(first.read_bytes()).hexdigest()}  {first.name}",
        f"{hashlib.sha256(second.read_bytes()).hexdigest()}  {second.name}",
    ]
