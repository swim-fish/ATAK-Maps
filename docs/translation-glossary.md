# 臺灣繁體中文翻譯對照表

本頁記錄 ATAK-Maps GitHub Pages 使用的中英對照詞彙。TAK 專有名詞以
`atak_docs` 的 `zh-TW` 詞彙資料為準；來源版本與 checksum 記錄於本專案的
`vendor/tak-terminology/README.md`。

## 已核准 TAK 詞彙

| English | 臺灣繁體中文 | 詞彙 ID |
|---|---|---|
| Import | 匯入 | `tak.import` |
| Download | 下載 | `tak.download` |
| Tap | 點選 | `tak.tap` |
| Select | 選取 | `tak.select` |
| Search | 搜尋 | `tak.search` |
| Add | 新增 | `tak.add` |
| View | 檢視 | `tak.view` |
| Publish | 發布 | `tak.publish` |
| Maps & Favorites | 地圖與我的最愛 | `atak.maps-favorites` |
| Tiles | 圖磚 | `atak.tiles` |
| Imagery | 影像 | `tak.imagery` |
| Data Package / Data Packages | 資料集 | `tak.data-package-data-packages` |
| Mission Package | Mission Package 資料集封裝格式 | `atak.mission-package` |
| Manifest | Manifest 套件清單 | `atak.manifest` |
| Overlays | 圖層 | `atak.overlays` |
| Overlay Manager | 圖層管理器 | `tak.overlay-manager` |
| Image Overlay / Image Overlays | 影像疊加層 | `tak.image-overlay-image-overlays` |
| Remote Resources | 遠端資源 | `atak.remote-resources` |
| Network Resources | 網路資源 | `atak.network-resources` |

## ATAK-Maps 專案用語

下列詞彙尚未收錄於上游核准詞彙表，先以本專案候選詞追蹤。後續若要
同步回 `atak_docs`，必須依該專案流程新增有來源的 `draft`，經審查後才能
標記為 `approved`。

| English | 臺灣繁體中文 | 狀態 | 使用範圍 |
|---|---|---|---|
| Map source | 地圖來源 | project candidate | 地圖服務 XML |
| Base map | 底圖 | project candidate | 非透明主要地圖 |
| Map layer | 地圖圖層 | project candidate | 地圖選擇器中的圖層 |
| Tile server | 圖磚伺服器 | project candidate | 網路圖磚服務 |
| Zoom level | 縮放層級 | project candidate | `minZoom`／`maxZoom` |
| Offline map | 離線地圖 | project candidate | 已下載供離線使用的地圖 |
| Map cache | 地圖快取 | project candidate | ATAK 本機圖磚快取 |
| Satellite | 衛星影像 | project candidate | Maps 分類 |
| Topographic | 地形圖 | project candidate | Maps 分類 |
| Street | 街道圖 | project candidate | Maps 分類 |
| Nautical | 航海圖 | project candidate | Maps 分類 |
| Cycling | 自行車 | project candidate | Maps 分類 |
| Land use | 土地利用 | project candidate | Maps 分類 |

## 翻譯規則

- 產品名稱、程式識別字、XML 元素名稱與檔名維持英文。
- 使用臺灣慣用詞，例如「軟體」「檔案」「資料」「設定」「網路」。
- ATAK 介面動作優先使用上表的核准詞，例如 `Tap` 譯為「點選」。
- `Mission Package` 保留英文產品術語，並依核准譯名補充「資料集封裝格式」。
- 新增或變更 TAK 專有名詞前，必須先查詢固定版本的詞彙資料。
