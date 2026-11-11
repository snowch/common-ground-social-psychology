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

Only `out/pages` is uploaded as the Pages artifact. It contains the course, 150 separate narration clips, PDFs, study companion, license notices, and ten offline chapter ZIPs. Audio loads on demand. Downloads embed the narration and include the continuous chapter recording. Every local URL is relative so it works under the repository path.

The build job checks media paths and hashes, local links, license notices, and chapter ZIP integrity before uploading. The separate deployment job requires `pages: write` and `id-token: write` and targets the `github-pages` environment. GitHub may require approval if the owner configures environment protection rules.

The owner authorized public publication after the current asset and license-notice checks passed. Pages and the repository are public; the separately hosted ChatGPT Site retains its own access settings. The copyright audit documents its evidence and limits; no legal certification is implied by deployment.
