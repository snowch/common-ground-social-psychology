# GitHub Pages deployment

The public course is hosted at:
https://snowch.github.io/common-ground-social-psychology/

GitHub Pages must use **GitHub Actions** as its build source. The `Deploy course to GitHub Pages` workflow builds and deploys on pushes to `main`; it also supports **Run workflow** in the Actions tab.

The build needs Python 3.12 and the committed course assets. No speech synthesis, paid API, secrets, or custom access token is needed. GitHub supplies its own short-lived token and deployment identity. Official checkout, Python, and Pages actions are pinned to commit hashes.

To build the same hosted files locally:

```sh
python3 build.py --portable --output out/portable
python3 scripts/build_hosted.py --output out/pages
python3 scripts/check_hosted.py --output out/pages
```

Only `out/pages` is uploaded as the Pages artifact. It contains the course, 168 separate narration clips, PDFs, study companion, license notices, and ten offline chapter ZIPs. Audio loads on demand. Downloads embed the narration and include the continuous chapter recording. Every local URL is relative so it works under the repository path.

The build job checks media paths and hashes, local links, license notices, and chapter ZIP integrity before uploading. The separate deployment job requires `pages: write` and `id-token: write` and targets the `github-pages` environment. GitHub may require approval if the owner configures environment protection rules.

The owner authorized public publication after the current asset and license-notice checks passed. Pages and the repository are public; the separately hosted ChatGPT Site retains its own access settings. The copyright audit documents its evidence and limits; no legal certification is implied by deployment.

## Browser offline option

The hosted header links to **Offline**. **Make available offline** explicitly saves the whole course in this browser (about 113 MB). No assets are precached merely by visiting. A completed save includes all 168 recordings, ten chapter decks, exercises, glossary, evidence notes, final case, study and visual companions and their PDFs. External research websites still need connectivity. ZIPs and continuous chapter tracks remain secondary file downloads.

Use HTTPS (or localhost for development). The service worker is scoped to the repository path; it never handles unrelated sites or deletes other applications' caches. `scripts/browser_offline.py` generates `offline-manifest.json` and pins each asset's SHA-256 and byte count in `sw.js`. Files are verified before caching. A release becomes active only after every file is saved. Interrupted saves resume; failed updates retain the complete old release. The prior release's recordings remain available for already-open tabs. Browser storage cleanup may remove the saved copy; users can check readiness, request browser persistence, update, or remove course files without removing learning progress.

To test locally after the hosted build:

```sh
python3 -m http.server 8891 --directory out/pages
python3 qa/check_browser_offline.py
python3 qa/check_offline_updates.py
```

The browser check covers all ten chapters with the network disabled, 197 cached files, narration and byte ranges, written responses, pause/resume, a browser restart, companions, mobile layouts, accessibility, and removal. The isolated update check injects corrupt files and verifies that an incomplete new release cannot replace a working offline course. `COURSE_BASE_URL` can point the browser check at the deployed site.
