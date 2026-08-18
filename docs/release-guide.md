# Making a Release

This guide explains the release process for ATAK-Maps. It covers how releases work in this repository and the steps required if you maintain your own fork.

## Release workflow overview

1. **Commit using Conventional Commits** – Only commits with prefixes such as `feat:` or `fix:` trigger a new release. Other prefixes like `docs:` or `chore:` will not publish a new version.
2. **Map Release workflow** – The repository has a workflow named *Map Release* that runs automatically on every push to `master` that changes XML files. It can also be run manually from the *Actions* tab. The workflow uses [semantic‑release](https://semantic-release.gitbook.io/semantic-release/) to determine the next [SemVer](https://semver.org/) version, tag the commit, and create the GitHub Release.
3. **ZIP assets** – As part of that same workflow, the complete, Taiwan-tested, and Taiwan Essential Data Packages are built and uploaded to the release entry.

The Taiwan archive is selected by `map-tests/taiwan-taichung.json`. Every map
XML must have an explicit entry in that profile; the build fails when the
profile is incomplete or contains a stale path.

`package-profiles/taiwan-essential.json` selects the recommended 14-source
package. Every release ZIP is a Manifest-bearing ATAK Mission Package v2 with
map entries under `content/` and `contentType="External Native Data"`.

## Releasing from a fork

If you maintain a fork, ensure you have GitHub Actions enabled. You may also need a personal access token with `contents: write` permission named `GH_TOKEN` or similar in your repository secrets. Follow these steps:

1. Merge your changes with a commit message that starts with `feat:` or `fix:`.
2. Run the *Map Release* workflow from the *Actions* tab. Select the branch you want to release from.
3. The workflow will use semantic‑release to tag your commit, build the ZIP, and create the GitHub Release.

## Troubleshooting

- **No release created** – Check that your commit messages use the lower-case prefix `feat:` or `fix:`. Upper-case variations are ignored by the release tools.
- **ZIP missing** – Ensure the *Map Release* workflow ran successfully and that `atak-maps.zip`, `atak-maps-taiwan.zip`, and `atak-maps-taiwan-essential.zip` appear as assets on the GitHub Release page.
