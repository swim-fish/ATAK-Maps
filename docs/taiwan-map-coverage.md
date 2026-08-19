# 臺灣地圖涵蓋範圍

本專案維護一份以臺灣為目標的測試結果，用來排除僅適用歐洲、北美洲，
或目前無法在臺灣正常顯示的來源。

## 測試位置與方式

- 地點：臺灣臺中市
- 座標：`24.161814640911395, 120.6468628683074`
- 測試日期：2026-08-18
- 範圍：全部 52 個地圖來源，從 XML 的 `minZoom` 測試至 `maxZoom`
- 請求數：1,008 次圖層請求
- 驗證項目：HTTP 回應、影像解碼及可見內容偵測

機器可讀的唯一事實來源是
[`map-tests/taiwan-taichung.json`](https://github.com/swim-fish/ATAK-Maps/blob/master/map-tests/taiwan-taichung.json)。
其中記錄各來源的實測縮放層級、目前有效範圍、最高層級結果、是否納入
臺灣測試版，以及判斷原因。

稀疏圖層在測試座標沒有地物時，可能回傳完全透明的圖磚。因此，自行車
路線、航標等全球稀疏圖層，在單一測試點無法證明全臺都沒有資料時仍會保留。

## 臺灣版本

| 版本 | 來源數 | 用途 |
|---|---:|---|
| 臺灣精選版 | 14 | Google、NLSC 與常用全球備援來源 |
| 臺灣測試版 | 32 | 在臺中測試點確認可用，或無法證明全臺無資料的來源 |
| 完整版本 | 52 | 全部來源，包含其他國家專用服務及需要 API 金鑰者 |

臺灣測試版的來源由 `map-tests/taiwan-taichung.json` 決定。新增、刪除或
重新命名 XML 後若沒有同步更新設定，打包會直接失敗。

臺灣精選版由 `package-profiles/taiwan-essential.json` 維護，目前包含 14 個
Google、國土測繪中心及備援來源。

## 臺灣測試版排除清單

`atak-maps-taiwan.zip` 目前排除以下 20 個來源：

| 地圖來源 | 排除原因 |
|---|---|
| basemap.de Raster, Farbe | 德國限定 WMS，在臺灣顯示空白 |
| basemap.de Raster, grau | 德國限定 WMS，在臺灣顯示空白 |
| BLM - Land Ownership (SMA) | 僅涵蓋美國 |
| BLM - Satellite + Land Ownership | 底圖可顯示，但 BLM 圖層在臺灣無內容 |
| BC Wildfire - Fire Perimeters | 僅涵蓋加拿大卑詩省 |
| FEMA NFHL - Flood Hazard Zones | 僅涵蓋美國，測試時連線遭重設 |
| GRG - BLM Public Lands Overlay | 僅涵蓋美國 |
| MTBMap.cz - MTB Map Europe | 詳細資料僅涵蓋歐洲 |
| NAIP - USDA CONUS Prime | 僅涵蓋美國本土，TLS 連線發生錯誤 |
| Canada Base Map - Transportation | 詳細資料僅涵蓋加拿大 |
| Canada - Toporama | 詳細資料僅涵蓋加拿大 |
| OpenSeaMap - Base Chart | 臺中測試點沒有可見內容 |
| OS - Light 3857 | 僅涵蓋英國，且需要 API 金鑰 |
| OS - Outdoor 3857 | 僅涵蓋英國，且需要 API 金鑰 |
| OS - Road 3857 | 僅涵蓋英國，且需要 API 金鑰 |
| PL Ortofoto Std | 僅涵蓋波蘭，連線逾時 |
| USGS - Usgsbasemap | 詳細資料僅涵蓋美國 |
| USGS - Usgsimageryonly | 詳細資料僅涵蓋美國 |
| USGS - Usgsimagerytopo | 詳細資料僅涵蓋美國 |
| USGS - Usgsshadedrelief | 詳細資料僅涵蓋美國 |

## 實測後修正的縮放範圍

| 地圖來源 | 原設定 | 目前有效範圍 |
|---|---:|---:|
| Bing - Hybrid | 0–20 | 1–20 |
| Bing - Maps | 0–20 | 1–20 |
| Bing - Satellite | 0–20 | 1–20 |
| CycleOSM - OSM Cycle | 0–21 | 0–20 |
| Esri - Clarity | 1–20 | 1–19 |
| GRG - Google Road Only Overlay | 0–20 | 2–20 |
| GRG - Google Terrain Shading Overlay | 0–20 | 0–18 |
| MTBMap.cz - MTB Map Europe | 0–21 | 0–18 |
| Taiwan - B5000 Topographic | 1–18 | 7–18 |
| Taiwan - EMAP96 | 1–19 | 8–19 |
| Taiwan - EMAP98 | 1–19 | 8–19 |
| Taiwan - Government Area Boundaries | 0–20 | 7–19 |
| Taiwan - Village Boundaries | 0–19 | 6–17 |

USGS、加拿大自然資源部等區域性來源仍保留服務原生的縮放範圍。臺灣
測試點顯示空白，只能證明該位置沒有內容，不能據此修改服務在原涵蓋區域的
有效範圍；這類來源會由臺灣版本設定排除。

## 建立資料集

執行：

```bash
python scripts/build_release_packages.py
```

命令會在 `dist/` 建立：

- `atak-maps-taiwan-essential.zip`：14 個臺灣精選來源
- `atak-maps-taiwan.zip`：32 個臺灣測試來源
- `atak-maps.zip`：全部 52 個來源
- `SHA256SUMS`：三個 ZIP 的 SHA-256 checksum

每個 ZIP 都包含一份 `MANIFEST/manifest.xml`；所有 XML 位於 `content/`，
並使用 ATAK `External Native Data` 內容類型。Release workflow 會上傳三個
資料集及 `SHA256SUMS`，Pages 產生器則以相同格式建立 `docs/pack/` 檔案。
