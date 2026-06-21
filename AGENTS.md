# AGENTS.md

This repository is a Hugo blog source tree for deployment to GitHub Pages.

Do not document or reintroduce the old AWS recovery workflow in normal changes. Treat the current repository state as the source of truth.

## Scope

- Main blog source: `site/`
- Hugo config: `site/hugo.yaml`
- GitHub Pages workflow: `.github/workflows/hugo.yaml`
- Recovery tooling under `tools/` and `tests/` exists for historical reconstruction and validation, but routine blog work should focus on Hugo content and GitHub Pages deployment.

## Repository model

- The production site is a Hugo site rooted at `site/`.
- The public URL target is `https://chadrick-kwag.github.io/`.
- `site/hugo.yaml` must keep `baseURL: https://chadrick-kwag.github.io/` unless the production domain changes.
- GitHub Pages deploys from GitHub Actions, not from committed static files.
- Do not commit `site/public/`.

## Content layout

- Posts live in `site/content/posts/<slug>/index.md`.
- Prefer page bundles:
  - `site/content/posts/<slug>/index.md`
  - `site/content/posts/<slug>/images/...`
- Use relative image references inside posts, for example:
  - `![](images/example.png)`

## New post rules

- Keep folder name and `slug` aligned when possible.
- Front matter should follow the current project convention:

```yaml
---
title: my new post
date: '2026-06-21T12:00:00+09:00'
lastmod: '2026-06-21T12:00:00+09:00'
slug: my-new-post
categories: []
tags: []
draft: true
---
```

- Start new posts with `draft: true`.
- Flip to `draft: false` only when ready to publish.

## Local development

- Run local dev server from the repository root:

```bash
.tools/bin/hugo server --source site --buildDrafts
```

- Default local URL:
  - `http://localhost:1313/`

- Production-style local build:

```bash
rm -rf site/public
.tools/bin/hugo --source site --panicOnWarning --minify
```

## Deployment model

- Deployment target: GitHub Pages user site
- Repository name: `chadrick-kwag.github.io`
- Default branch: `main`
- Workflow file: `.github/workflows/hugo.yaml`
- Deployment happens on push to `main`

The workflow:

- installs Hugo Extended
- builds with `--source site`
- injects the Pages `base_url` at build time
- uploads `site/public`
- deploys with `actions/deploy-pages`

## Required checks before pushing content or config changes

Run these from the repository root:

```bash
rm -rf site/public
.tools/bin/hugo --source site --panicOnWarning --minify
git diff --check
git status --short
```

Expected:

- Hugo build exits successfully
- `git diff --check` prints nothing
- `git status --short` only shows intentional changes

## Files and directories to avoid committing

These are local-only or generated artifacts:

- `.env`
- `temp/`
- `backup/`
- `manifests/`
- `reports/`
- `site/public/`

If a task regenerates local artifacts, do not add them back to git.

## What to change for normal blog work

Usually change only:

- `site/content/posts/**`
- `site/content/_index.md`
- `site/content/archives.md`
- `site/content/search.md`
- `site/hugo.yaml`
- `.github/workflows/hugo.yaml`

Avoid changing recovery code unless the task is specifically about recovery or validation tooling.
