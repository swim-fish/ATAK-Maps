# 發布新版本

本指南說明 ATAK-Maps 的 GitHub Release 流程，以及 fork 維護者需要的設定。

## 發布流程

1. **使用 Conventional Commits**：`feat:` 產生 Minor 版本，`fix:` 與
   `perf:` 產生 Patch 版本。`docs:`、`ci:` 及 `chore:` 不會單獨發布。
2. **Map Release workflow**：每次推送到 `master` 都會執行。semantic-release
   會分析上一個 tag 之後的 commit，判斷是否需要新 SemVer 版本。
3. **建立資料集**：workflow 會產生完整版本、臺灣測試版、臺灣精選版及
   `SHA256SUMS`。
4. **建立 GitHub Release**：semantic-release 建立 tag、更新
   `CHANGELOG.md`，再將四個檔案附加至 Release。

同一批檔案也會以 `atak-map-release-files` workflow artifact 保留 14 天，
方便在沒有產生新版本時檢查打包結果。

## Release 檔案

| 檔案 | 內容 |
|---|---|
| `atak-maps-taiwan-essential.zip` | 14 個臺灣精選來源，建議一般使用者安裝 |
| `atak-maps-taiwan.zip` | 32 個臺灣測試來源 |
| `atak-maps.zip` | 全部 52 個來源 |
| `SHA256SUMS` | 三個 ZIP 的 SHA-256 checksum |

每個 ZIP 都是 ATAK Mission Package v2 資料集。地圖 XML 位於
`content/`，`MANIFEST/manifest.xml` 會將每個來源宣告為
`External Native Data`。

臺灣測試版由 `map-tests/taiwan-taichung.json` 決定。每個 XML 都必須有
明確設定，否則打包失敗。臺灣精選版則由
`package-profiles/taiwan-essential.json` 維護。

## Fork 設定

1. 啟用 GitHub Actions。
2. 在 repository 的 Actions 設定允許 workflow 使用 `contents: write`。
3. 確認 `master` branch protection 允許 GitHub Actions 建立 tag 及推送
   semantic-release 產生的 changelog commit。
4. 使用 `feat:` 或 `fix:` commit 合併變更。
5. 等候 *Map Release* 自動執行，或從 Actions 分頁手動執行。

workflow 使用 GitHub 自動產生的 `GITHUB_TOKEN`。除非 branch protection
禁止該 token 推送，否則不需要額外建立 personal access token。

## 穩定下載網址

最新 Release 會固定提供下列網址：

- [臺灣精選版](https://github.com/swim-fish/ATAK-Maps/releases/latest/download/atak-maps-taiwan-essential.zip)
- [臺灣測試版](https://github.com/swim-fish/ATAK-Maps/releases/latest/download/atak-maps-taiwan.zip)
- [完整版本](https://github.com/swim-fish/ATAK-Maps/releases/latest/download/atak-maps.zip)
- [SHA256SUMS](https://github.com/swim-fish/ATAK-Maps/releases/latest/download/SHA256SUMS)

## 疑難排解

- **沒有建立 Release**：確認 commit 使用小寫 `feat:`、`fix:` 或 `perf:`，
  並確認 repository 已有正確的版本 tag 基準。
- **Release 缺少檔案**：檢視 *Build map ZIPs*、*Upload release candidates*
  與 *semantic-release* 步驟。
- **無法推送 changelog commit**：檢查 branch protection 及 workflow 的
  `contents: write` 權限。
- **tag 不在目前 branch**：workflow 會在 *Verify tag ancestry* 直接停止，
  以避免在重寫歷史後發布錯誤版本。
