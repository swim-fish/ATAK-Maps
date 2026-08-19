# 安裝 ATAK 地圖

## 快速開始

1. 下載建議使用的 [臺灣精選版](https://github.com/swim-fish/ATAK-Maps/releases/latest/download/atak-maps-taiwan-essential.zip)、[臺灣測試版](https://github.com/swim-fish/ATAK-Maps/releases/latest/download/atak-maps-taiwan.zip)或[完整版](https://github.com/swim-fish/ATAK-Maps/releases/latest/download/atak-maps.zip)。
2. 在 ATAK 中使用「匯入」開啟 ZIP；ATAK 會自動放置地圖檔案。
3. 完成後，地圖來源會顯示於「地圖與我的最愛」。

ATAK 的匯入功能會處理檔案位置，不必手動解壓縮。

![安裝流程](images/install-flow.png)

## 使用 ATAK 匯入（建議）

1. 將 ZIP 下載到 ATAK 裝置。
2. 在 ATAK 點選「匯入」，或從檔案管理程式以 ATAK 開啟 ZIP。
3. ATAK 會讀取資料集並自動加入地圖來源。
4. 開啟「地圖與我的最愛」，確認新來源已出現。

### 選擇版本

| 版本 | 檔案 | 來源數 | 適合對象 |
|---|---|---:|---|
| 臺灣精選版 | `atak-maps-taiwan-essential.zip` | 14 | 大多數臺灣使用者；包含 Google、NLSC 與備援來源 |
| 臺灣測試版 | `atak-maps-taiwan.zip` | 32 | 需要更多全球來源，且只保留臺灣測試結果可用者 |
| 完整版本 | `atak-maps.zip` | 52 | 需要其他國家圖資或自行設定 API 金鑰者 |

每個 ZIP 都是 ATAK Mission Package v2 資料集，內含一份
`MANIFEST/manifest.xml`。地圖 XML 位於 `content/`，並宣告為 ATAK
`External Native Data`。

Release 另附
[`SHA256SUMS`](https://github.com/swim-fish/ATAK-Maps/releases/latest/download/SHA256SUMS)，
可確認下載檔案完整且未遭變更。

## 手動安裝

若只想安裝特定 XML，或裝置無法使用 ZIP 匯入，可手動放置檔案。

![目錄配置](images/directory-layout.png)

### 底圖

將一般地圖來源 XML 複製到：

```text
<storage>/atak/imagery/mobile/mapsources/
```

`<storage>` 是裝置的內部儲存空間根目錄，通常是 `/sdcard` 或
`/storage/emulated/0`。ATAK 也支援
`<storage>/atak/mobac/mapsources/`。

### 圖層

將 `GRG/` 目錄內以 `grg_` 開頭的 XML 複製到：

```text
<storage>/atak/grg/
```

這些檔案會顯示為可疊加的圖層，不會列為底圖。

### 驗證安裝

1. 開啟 ATAK。
2. 點選圖層圖示，開啟「地圖與我的最愛」。
3. 選取新地圖，確認圖磚能正常載入。
4. 若是透明圖層，請在「圖層管理器」中確認。

ATAK 會監控地圖目錄，通常不必重新啟動。若來源沒有出現，請重新啟動
ATAK，再檢查檔案位置。

## 安裝單一地圖來源

1. 在 [GitHub 專案](https://github.com/swim-fish/ATAK-Maps)中找到來源目錄。
2. 只下載需要的 `.xml` 檔案。
3. 使用 ATAK 匯入，或依前述目錄手動放置。

## 建立離線地圖快取

ATAK 會自動快取已檢視的圖磚。若要事先下載任務區域：

1. 開啟「地圖與我的最愛」，選取要下載的地圖來源。
2. 進入 Map Manager，或長按地圖圖層。
3. 點選「下載」，並在地圖上框選範圍。
4. 選取需要的縮放層級後開始下載。
5. ATAK 會將圖磚儲存於裝置的 SQLite 資料庫，離線後仍可使用。

下載前請確認來源服務的使用條款允許離線快取。

## 疑難排解

### 匯入後沒有顯示地圖

- 重新啟動 ATAK。
- 手動安裝時，確認 XML 位於正確目錄。
- 在 ATAK 的「設定 > 顯示記錄」檢視載入錯誤。
- 確認 ZIP 內有 `MANIFEST/manifest.xml`，且不是一般壓縮檔。

### 圖磚呈現黑色或空白

- 地圖伺服器可能暫時離線或阻擋 ATAK 請求。
- 檢查裝置網路連線與系統時間。
- 部分 OpenStreetMap 服務會限制大量或非瀏覽器請求。
- 區域性來源在臺灣顯示空白不代表服務故障；請參考
  [臺灣涵蓋範圍](taiwan-map-coverage.md)。

### 手動安裝目錄錯誤

| 檔案類型 | 正確目錄 | 常見錯誤 |
|---|---|---|
| 底圖（`.xml`） | `atak/imagery/mobile/mapsources/` | 放在不會掃描的上層 `atak/imagery/` |
| 圖層（`grg_*.xml`） | `atak/grg/` | 放入底圖目錄 |

### 支援的副檔名

| 副檔名 | 說明 |
|---|---|
| `.xml` | 標準地圖來源；本專案主要提供此格式 |
| `.xmle` | 加密 XML 地圖來源 |
| `.bsh` | BeanShell 指令碼地圖來源 |
