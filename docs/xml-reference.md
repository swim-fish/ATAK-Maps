# MOBAC XML 參考

## 概觀

ATAK 使用 MOBAC 相容 XML 定義線上地圖來源。本專案支援三種根元素：

| 根元素 | 用途 | 常見情境 |
|---|---|---|
| `customMapSource` | TMS、XYZ 或 quadkey 圖磚 | Google、Bing、Esri、OSM 類服務 |
| `customWmsMapSource` | OGC Web Map Service（WMS） | 政府 GIS、ArcGIS WMS |
| `customMultiLayerMapSource` | 組合多個地圖來源 | 衛星影像加道路或透明圖層 |

XML 宣告應使用 UTF-8：

```xml
<?xml version="1.0" encoding="UTF-8"?>
```

## `customMapSource`：TMS／XYZ 圖磚

### 元素

| 元素 | 類型 | 必要 | 預設值 | 說明 |
|---|---|---|---|---|
| `name` | 字串 | 是 | — | ATAK 顯示的地圖名稱 |
| `url` | 字串 | 是 | — | 含[網址預留位置](#url-placeholders)的圖磚範本 |
| `maxZoom` | 整數 | 是 | — | 最高縮放層級，包含該層級 |
| `minZoom` | 整數 | 否 | `0` | 最低縮放層級，包含該層級 |
| `tileType` | 字串 | 否 | 無 | 影像格式提示，例如 `png`、`jpg` |
| `tileUpdate` | 字串／整數 | 否 | `0` | [快取更新](#cache-refresh)間隔 |
| `serverParts` | 字串 | 否 | 無 | 以空白分隔的[伺服器分流](#server-parts)值 |
| `invertYCoordinate` | 布林值 | 否 | `false` | TMS 左下原點服務設為 `true` |
| `backgroundColor` | 色碼 | 否 | `#000000` | `#RRGGBB` 背景色 |
| `coordinatesystem` | 字串 | 否 | `EPSG:3857` | [座標系統](#coordinate-systems) |

### 完整範例

```xml
<?xml version="1.0" encoding="UTF-8"?>
<customMapSource>
    <name>OpenTopo - Opentopomap</name>
    <minZoom>1</minZoom>
    <maxZoom>17</maxZoom>
    <tileType>png</tileType>
    <url>https://a.tile.opentopomap.org/{$z}/{$x}/{$y}.png</url>
    <tileUpdate>None</tileUpdate>
    <backgroundColor>#000000</backgroundColor>
</customMapSource>
```

實際檔案：
[`opentopo/opentopo_opentopomap.xml`](https://github.com/swim-fish/ATAK-Maps/blob/master/opentopo/opentopo_opentopomap.xml)。

### Bing quadkey 範例

```xml
<customMapSource>
    <name>Bing - Satellite</name>
    <minZoom>1</minZoom>
    <maxZoom>20</maxZoom>
    <tileType>jpg</tileType>
    <url>https://ecn.t{$serverpart}.tiles.virtualearth.net/tiles/a{$q}.jpeg?g=1&amp;n=z</url>
    <serverParts>0 1 2 3</serverParts>
</customMapSource>
```

XML 屬性與文字中的 `&` 必須寫成 `&amp;`。

## `customWmsMapSource`：WMS

### 元素

| 元素 | 類型 | 必要 | 預設值 | 說明 |
|---|---|---|---|---|
| `name` | 字串 | 是 | — | 顯示名稱 |
| `url` | 字串 | 是 | — | WMS 基礎網址 |
| `layers` | 字串 | 是 | — | 以逗號分隔的 WMS 圖層名稱 |
| `maxZoom` | 整數 | 是 | — | 最高縮放層級 |
| `tileType` | 字串 | 是 | — | `PNG` 或 `JPG` |
| `minZoom` | 整數 | 否 | `-1` | 最低縮放層級；WMS 預設不是 `0` |
| `styles` | 字串 | 否 | 空字串 | WMS `STYLES` 參數 |
| `version` | 字串 | 否 | `1.1.1` | `1.1.1`、`1.3.0` 或 `1.3.1` |
| `coordinatesystem` | 字串 | 否 | `EPSG:4326` | WMS 座標系統 |
| `aditionalparameters` | 字串 | 否 | 空字串 | 附加至 GetMap 的查詢參數；ATAK 原始拼字 |
| `additionalparameters` | 字串 | 否 | 空字串 | 正確拼字，ATAK 也接受 |
| `backgroundColor` | 色碼 | 否 | `#000000` | 背景色 |
| `north`、`south`、`east`、`west` | 小數 | 否 | 無 | 地理界線；四個值必須同時設定 |
| `tileUpdate` | 字串／整數 | 否 | `0` | 快取更新間隔 |

### WMS 版本差異

| 版本 | CRS 參數 | SRID 4326 使用值 | 軸順序 |
|---|---|---|---|
| `1.1.1` | `srs=EPSG:4326` | `EPSG:4326` | x、y |
| `1.3.0` | `crs=CRS:84` | `CRS:84` | x、y |
| `1.3.1` | `crs=CRS:84` | `CRS:84` | x、y |

ATAK 會自動產生 `SERVICE=WMS`、`REQUEST=GetMap`、`WIDTH=256`、
`HEIGHT=256`、`BBOX`、`FORMAT`、`LAYERS`、`STYLES` 及版本參數。

### CDATA

含多個 `&` 的網址可使用 CDATA，避免逐一改寫成 XML entity：

```xml
<url><![CDATA[https://example.gov/wms?token=a&mode=map&]]></url>
```

### 完整範例

```xml
<?xml version="1.0" encoding="UTF-8"?>
<customWmsMapSource>
    <name>FEMA NFHL - Flood Hazard Zones</name>
    <minZoom>5</minZoom>
    <maxZoom>19</maxZoom>
    <tileType>PNG</tileType>
    <version>1.3.0</version>
    <layers>28</layers>
    <styles></styles>
    <url>https://hazards.fema.gov/gis/nfhl/rest/services/public/NFHL/MapServer/export?</url>
    <coordinatesystem>EPSG:3857</coordinatesystem>
</customWmsMapSource>
```

### `tileType` 對應

| `tileType` | WMS `FORMAT` |
|---|---|
| `PNG` | `image/png` |
| `JPG` | `image/jpeg` |

## `customMultiLayerMapSource`：多圖層組合

多圖層來源會依 XML 順序由下往上繪製子來源。

| 元素 | 類型 | 必要 | 預設值 | 說明 |
|---|---|---|---|---|
| `name` | 字串 | 是 | — | 顯示名稱 |
| `layers` | 容器 | 是 | — | 內含其他地圖來源元素 |
| `backgroundColor` | 色碼 | 否 | `#000000` | 最先繪製的背景色 |
| `layersAlpha` | 字串 | 否 | 全部 `1.0` | 各圖層透明度，以空白分隔 |

`layersAlpha` 的值必須介於 `0.0` 與 `1.0`，數量必須與子圖層相同。
組合後輸出固定為 256 × 256 PNG。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<customMultiLayerMapSource>
    <name>Google Satellite + Roads</name>
    <backgroundColor>#000000</backgroundColor>
    <layersAlpha>1.0 1.0</layersAlpha>
    <layers>
        <customMapSource>
            <name>Satellite</name>
            <minZoom>0</minZoom>
            <maxZoom>20</maxZoom>
            <tileType>jpg</tileType>
            <url>https://mt{$serverpart}.google.com/vt/lyrs=s&amp;x={$x}&amp;y={$y}&amp;z={$z}</url>
            <serverParts>0 1 2 3</serverParts>
        </customMapSource>
        <customMapSource>
            <name>Roads</name>
            <minZoom>0</minZoom>
            <maxZoom>20</maxZoom>
            <tileType>png</tileType>
            <url>https://mt{$serverpart}.google.com/vt/lyrs=h&amp;x={$x}&amp;y={$y}&amp;z={$z}</url>
            <serverParts>0 1 2 3</serverParts>
        </customMapSource>
    </layers>
</customMultiLayerMapSource>
```

## 網址預留位置 { #url-placeholders }

| 預留位置 | ATAK 替代內容 | 範例 |
|---|---|---|
| `{$z}` | 縮放層級 | `14` |
| `{$x}` | 圖磚欄號 | `8567` |
| `{$y}` | 圖磚列號；預設以左上為原點 | `5765` |
| `{$q}` | Bing quadkey | `12031021230` |
| `{$serverpart}` | `serverParts` 的下一個值 | `a` |

### Quadkey

Quadkey 會依每一層的 x、y 位元產生 `0` 至 `3` 的字串。`{$q}` 的長度
等於縮放層級。一般來源不需自行計算，ATAK 會在傳送請求前替換。

## 伺服器分流（`serverParts`） { #server-parts }

`serverParts` 以空白分隔，ATAK 會輪流替換 `{$serverpart}`：

```xml
<serverParts>a b c</serverParts>
<url>https://{$serverpart}.tile.example.com/{$z}/{$x}/{$y}.png</url>
```

這只會分散請求，不會改變圖磚座標。若網址沒有 `{$serverpart}`，設定不會
產生效果。

## 座標系統 { #coordinate-systems }

| SRID | 名稱 | 說明 |
|---|---|---|
| `EPSG:3857` | Web Mercator | `customMapSource` 預設值，常見網路圖磚格式 |
| `EPSG:4326` | WGS 84 | `customWmsMapSource` 預設值，經緯度座標 |
| `EPSG:900913` | 舊式 Web Mercator | `EPSG:3857` 別名 |

元素名稱大小寫必須符合 ATAK parser。一般地圖使用小寫
`coordinatesystem`；不要自行改成 `coordinateSystem`。

## 快取更新 { #cache-refresh }

| `tileUpdate` | 行為 |
|---|---|
| `0` 或省略 | 不自動重新整理；圖磚持續保留於 ATAK SQLite 快取 |
| 正整數 | 重新整理間隔，單位為毫秒，例如 `604800000` 為 7 天 |
| `None` | 非數值，parser 會忽略，等同 `0` |
| `IfNoneMatch` | 非數值，parser 會忽略，等同 `0` |

## HTTP 行為

| 設定 | ATAK 行為 | XML 可否設定 |
|---|---|---|
| `User-Agent` | `TAK` | 否 |
| `x-common-site-name` | 自動使用 `name` | 否 |
| 連線逾時 | 3,000 ms | 只能由程式 `Config` 設定 |
| 讀取逾時 | 5,000 ms | 只能由程式 `Config` 設定 |
| 快取 | `setUseCaches(true)` | 否 |

### TLS 與驗證

- 使用 ATAK 支援的 HTTPS 憑證鏈與 TLS 版本。
- XML 本身沒有通用的自訂 HTTP header 元素。
- 不可將私人 API 金鑰提交至公開 repository；請使用 `API_KEY_HERE`。
- Basic Auth 可以放入網址，但不建議在公開 XML 儲存憑證。

## 已知相容性注意事項

### `aditionalparameters` 拼字

ATAK 歷史 parser 使用少一個 `d` 的 `aditionalparameters`。目前也接受
`additionalparameters`，但舊版 ATAK 可能只認得原始拼字。

### `coordinatesystem` 大小寫

ATAK 使用全小寫元素名稱。MOBAC 或其他工具產生的 `coordinateSystem`
不一定能被 ATAK 讀取。

### `tileUpdate` 字串

雖然部分範例使用 `None` 或 `IfNoneMatch`，只有整數會實際設定更新間隔。

### 固定圖磚大小

ATAK 以 256 × 256 圖磚運作。XML 沒有可調整圖磚大小的元素。

### `tileType` 與 `ignoreErrors`

- `customMapSource` 的 `tileType` 不會由 parser 嚴格驗證，但仍應符合回傳格式。
- MOBAC 的 `ignoreErrors` 不會被 ATAK parser 使用。

### XML entity

XML 必須是 well-formed。查詢字串中的 `&` 請改成 `&amp;` 或使用 CDATA；
不要使用未定義的 HTML entity。

### WMS 網址

WMS `url` 最好以 `?` 或 `&` 結尾，讓 ATAK 安全附加 GetMap 參數。

## 快速比較

| 元素 | `customMapSource` | `customWmsMapSource` | `customMultiLayerMapSource` |
|---|---|---|---|
| `name` | 必要 | 必要 | 必要 |
| `url` | 必要 | 必要 | — |
| `maxZoom` | 必要 | 必要 | 由子圖層推導 |
| `minZoom` | 選用，預設 `0` | 選用，預設 `-1` | 由子圖層推導 |
| `tileType` | 選用 | 必要 | 固定 PNG |
| `layers` | — | WMS 圖層名稱 | 必要的子來源容器 |
| `tileUpdate` | 選用 | 選用 | — |
| `serverParts` | 選用 | — | — |
| `invertYCoordinate` | 選用 | — | — |
| `backgroundColor` | 選用 | 選用 | 選用 |
| `coordinatesystem` | 預設 3857 | 預設 4326 | — |
| `layersAlpha` | — | — | 選用 |

## 驗證

本專案的 XSD 位於
[`schema/mobac-maps.xsd`](https://github.com/swim-fish/ATAK-Maps/blob/master/schema/mobac-maps.xsd)。

在 Linux 或 GitHub Actions 可執行：

```bash
xmllint --noout --schema schema/mobac-maps.xsd path/to/map.xml
```

也可以執行完整語意驗證：

```bash
python -m mapvalidator
```

XSD 能檢查結構與資料類型，但無法保證遠端服務可連線、API 金鑰有效，或
特定區域有可見內容。要加入臺灣版本時，仍需依
[臺灣涵蓋範圍](taiwan-map-coverage.md)的方法實際測試。
