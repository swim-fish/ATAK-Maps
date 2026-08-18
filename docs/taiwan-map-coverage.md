# Taiwan Map Coverage Profile

This repository maintains a Taiwan-tested package profile for deployments that
do not need map sources limited to Europe or North America.

## Test location and method

- Location: Taichung, Taiwan
- Coordinate: `24.161814640911395, 120.6468628683074`
- Test date: 2026-08-18
- Scope: all 52 map sources, from each XML file's `minZoom` through `maxZoom`
- Requests: 1,008 layer requests
- Validation: HTTP success, image decoding, and visible-content detection

The machine-readable source of truth is
[`map-tests/taiwan-taichung.json`](https://github.com/joshuafuller/ATAK-Maps/blob/master/map-tests/taiwan-taichung.json). It
records the observed zoom levels, current effective range, maximum-zoom result,
package decision, and decision reason for every XML source.

Sparse overlays can return a transparent tile when no feature crosses the
sample coordinate. Global sparse overlays such as cycle routes and seamarks are
therefore retained when the test cannot prove Taiwan-wide absence.

## Package selection

The Taiwan package currently contains 32 sources and excludes 20 sources.
Every XML file must have an explicit profile entry. Package generation fails if
a source is added, removed, or renamed without updating the profile.

The recommended Taiwan Essential package is a separate curated subset of 14
Google, Taiwan NLSC, and fallback sources. Its source of truth is
`package-profiles/taiwan-essential.json`.

The following sources are excluded from `atak-maps-taiwan.zip`:

| Source | Reason |
|---|---|
| basemap.de Raster, Farbe | Germany-only WMS; blank in Taiwan |
| basemap.de Raster, grau | Germany-only WMS; blank in Taiwan |
| BLM - Land Ownership (SMA) | United States-only overlay |
| BLM - Satellite + Land Ownership | Base displayed, but the BLM overlay did not |
| BC Wildfire - Fire Perimeters | British Columbia-only overlay |
| FEMA NFHL - Flood Hazard Zones | United States-only; connections reset |
| GRG - BLM Public Lands Overlay | United States-only overlay |
| MTBMap.cz - MTB Map Europe | Europe-only detailed coverage |
| NAIP - USDA CONUS Prime | United States-only; TLS failures |
| Canada Base Map - Transportation | Canada-only detailed coverage |
| Canada - Toporama | Canada-only detailed coverage |
| OpenSeaMap - Base Chart | No visible content at the Taichung sample |
| OS - Light 3857 | Great Britain-only and requires an API key |
| OS - Outdoor 3857 | Great Britain-only and requires an API key |
| OS - Road 3857 | Great Britain-only and requires an API key |
| PL Ortofoto Std | Poland-only; connection timeouts |
| USGS - Usgsbasemap | United States-only detailed coverage |
| USGS - Usgsimageryonly | United States-only detailed coverage |
| USGS - Usgsimagerytopo | United States-only detailed coverage |
| USGS - Usgsshadedrelief | United States-only detailed coverage |

## Zoom corrections from the test

| Source | Previous | Effective |
|---|---:|---:|
| Bing - Hybrid | 0-20 | 1-20 |
| Bing - Maps | 0-20 | 1-20 |
| Bing - Satellite | 0-20 | 1-20 |
| CycleOSM - OSM Cycle | 0-21 | 0-20 |
| Esri - Clarity | 1-20 | 1-19 |
| GRG - Google Road Only Overlay | 0-20 | 2-20 |
| GRG - Google Terrain Shading Overlay | 0-20 | 0-18 |
| MTBMap.cz - MTB Map Europe | 0-21 | 0-18 |
| Taiwan - B5000 Topographic | 1-18 | 7-18 |
| Taiwan - EMAP96 | 1-19 | 8-19 |
| Taiwan - EMAP98 | 1-19 | 8-19 |
| Taiwan - Government Area Boundaries | 0-20 | 7-19 |
| Taiwan - Village Boundaries | 0-19 | 6-17 |

Regional sources such as USGS and Natural Resources Canada retain their native
zoom ranges. A blank Taiwan tile does not establish the service's valid range
inside its intended region; these sources are excluded by the package profile
instead.

## Building packages

Run:

```bash
python scripts/build_release_packages.py
```

The command writes ATAK Mission Package v2 ZIP archives:

- `dist/atak-maps-taiwan-essential.zip` — 14 common Taiwan sources
- `dist/atak-maps-taiwan.zip` — the 32 sources approved by this profile
- `dist/atak-maps.zip` — all 52 sources

Each ZIP contains one `MANIFEST/manifest.xml`; all XML sources live below
`content/` and use the ATAK `External Native Data` content type. The release
workflow uploads all three archives, and the Pages generator creates the same
Data Package format under `docs/pack/`.
