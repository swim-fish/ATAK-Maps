# 建立自訂地圖來源

本指南說明如何建立第一個 ATAK 地圖來源 XML，並提交至本專案。完整元素
規格請參考 [MOBAC XML 參考](xml-reference.md)。

## 建立第一個地圖來源

### 1. 找到圖磚伺服器網址

公開圖磚服務通常使用 `{z}/{x}/{y}` 網址格式。常見來源包含
[OpenStreetMap 圖磚服務清單](https://wiki.openstreetmap.org/wiki/Raster_tile_providers)
及政府 GIS 入口網站。使用前請確認服務條款允許第三方應用程式存取與離線快取。

### 2. 建立 XML 檔案

每個 `customMapSource` 至少需要 `name`、`url` 及 `maxZoom`。建議同時設定
`minZoom`、`tileType` 與 `backgroundColor`。

### 3. 完整範例

```xml
<?xml version="1.0" encoding="UTF-8"?>
<customMapSource>
    <name>OpenTopo - Opentopomap</name>
    <minZoom>1</minZoom>
    <maxZoom>17</maxZoom>
    <tileType>png</tileType>
    <url>https://a.tile.opentopomap.org/{$z}/{$x}/{$y}.png</url>
    <backgroundColor>#000000</backgroundColor>
</customMapSource>
```

![XML 元素說明](images/xml-anatomy.png)

注意事項：

- ATAK 執行時會以圖磚座標取代 `{$z}`、`{$x}`、`{$y}`。
- `tileType` 必須符合伺服器實際回傳格式，例如 `png` 或 `jpg`。
- `maxZoom` 不可超過服務實際提供的最高縮放層級。
- 若服務需要 API 金鑰，請保留 `API_KEY_HERE`，不可提交私人金鑰。

## 在 ATAK 測試

1. 將 XML 複製到 `atak/imagery/mobile/mapsources/`。
2. 開啟 ATAK，在「地圖與我的最愛」尋找 XML 中的 `name`。
3. 平移並切換各縮放層級，確認圖磚能正常載入。
4. 若要提供臺灣版本，請在臺中測試座標
   `24.161814640911395, 120.6468628683074` 測試至 `maxZoom`。

其他安裝方式請參考[安裝指南](install-guide.md)。

## 提交至 ATAK-Maps

1. Fork [本專案](https://github.com/swim-fish/ATAK-Maps)，再建立新 branch。
2. 將 XML 放入對應的服務提供者目錄，例如 `opentopo/`。
3. 同步更新 `descriptions.yml` 的臺灣繁體中文簡介。
4. 若來源要加入臺灣版本，更新 `map-tests/taiwan-taichung.json`；臺灣精選版
   另需更新 `package-profiles/taiwan-essential.json`。
5. 使用 Conventional Commits，例如 `feat: add <map name>`。
6. 建立 pull request。

完整貢獻規範請參考
[CONTRIBUTING.md](https://github.com/swim-fish/ATAK-Maps/blob/master/CONTRIBUTING.md)。

## 下一步

- [MOBAC XML 參考](xml-reference.md)：WMS、多圖層、伺服器分流、座標系統及元素說明。
- [安裝指南](install-guide.md)：匯入、手動安裝及離線地圖快取。
- [臺灣涵蓋範圍](taiwan-map-coverage.md)：測試方式與版本納入條件。
