"""Guard the pinned zh-TW terminology snapshot used by GitHub Pages."""

import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
GLOSSARY = REPO_ROOT / "vendor" / "tak-terminology" / "glossary.zh-TW.json"
EXPECTED_SHA256 = "3e8af6cb57aa7f2dfd85171b993cb4e7b0b49d2f19342e60eb0d4872b7a458ed"


def test_terminology_snapshot_metadata_and_checksum():
    payload = GLOSSARY.read_bytes()
    data = json.loads(payload)

    assert hashlib.sha256(payload).hexdigest() == EXPECTED_SHA256
    assert data["schemaVersion"] == 1
    assert data["dataVersion"] == "1.0.0"
    assert data["locale"] == "zh-TW"


def test_pages_terms_match_approved_atak_translations():
    terms = json.loads(GLOSSARY.read_text(encoding="utf-8"))["terms"]

    expected = {
        "tak.import": "匯入",
        "tak.download": "下載",
        "tak.tap": "點選",
        "tak.select": "選取",
        "tak.search": "搜尋",
        "tak.add": "新增",
        "tak.view": "檢視",
        "tak.publish": "發布",
        "atak.maps-favorites": "地圖與我的最愛",
        "atak.tiles": "圖磚",
        "tak.imagery": "影像",
        "tak.data-package-data-packages": "資料集",
        "atak.overlays": "圖層",
        "tak.overlay-manager": "圖層管理器",
    }

    assert {term_id: terms[term_id]["translation"] for term_id in expected} == expected
