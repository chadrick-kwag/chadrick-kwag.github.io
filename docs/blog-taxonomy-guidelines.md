# Blog Taxonomy Guidelines

This document defines the working rules for `categories` and `tags` across blog posts under `site/content/posts/`.

## Goals

- Keep `categories` small, stable, and useful for browsing.
- Keep `tags` specific and useful for search/discovery.
- Avoid duplicate labels and inconsistent naming.

## Categories

Use these categories only:

- `paper-review`
- `machine-learning`
- `python`
- `web`
- `linux`
- `devops`
- `database`
- `tools`

### Category Rules

- Every post should have exactly 1 category unless a second category is clearly justified.
- Prefer 1 category for most posts.
- Use at most 2 categories on any post.
- Do not invent new categories without revisiting this document.

### Category Meanings

- `paper-review`: paper reviews and paper summaries.
- `machine-learning`: model training, CV, NLP, CUDA, PyTorch, TensorFlow, ONNX, TensorRT, and ML implementation topics.
- `python`: general Python language usage, scripting, standard library usage, and Python-specific snippets not primarily about ML.
- `web`: Hugo, JavaScript, TypeScript, React, Vue, frontend, browser APIs, and web app behavior.
- `linux`: Ubuntu, shell, package management, desktop/system configuration, drivers, and Linux troubleshooting.
- `devops`: Docker, proxy/network deployment topics, CI/CD, infrastructure, and environment/runtime setup for services.
- `database`: PostgreSQL, MySQL, PySpark SQL/data querying topics, and database operations.
- `tools`: IDE/editor usage, Jupyter, git usage, productivity tools, and standalone utilities that do not fit better elsewhere.

### Category Precedence

When a post could fit multiple categories, use this precedence:

1. If it is a paper review or summary, include `paper-review`.
2. If it is primarily about ML frameworks, training, inference, or CUDA stack behavior, prefer `machine-learning`.
3. If it is primarily language or scripting usage in Python, prefer `python`.
4. If it is primarily browser/frontend/Hugo behavior, prefer `web`.
5. If it is primarily OS/package/shell/system configuration, prefer `linux`.
6. If it is primarily container/deployment/proxy/infra behavior, prefer `devops`.
7. If it is primarily DB/query/storage behavior, prefer `database`.
8. Use `tools` for editor/IDE/git/Jupyter/tooling topics that do not fit better elsewhere.

## Tags

Tags are post-specific and may vary more than categories, but they must follow consistent naming.

### Tag Rules

- Use lowercase `kebab-case` only.
- Prefer canonical full names over abbreviations.
- Use 2 to 5 tags per post in most cases.
- Tags should describe concrete technologies, libraries, methods, protocols, or problem types.
- Do not repeat a category as a tag unless it adds real search value.
- Avoid vague tags such as `error`, `tips`, `example`, or `config`.
- Reclassify tags from post meaning first; do not preserve old tags by default.

### Canonical Naming Rules

- Use `tensorflow`, not `tf`.
- Use `javascript`, not `js`.
- Use `visual-studio-code` or `vscode`, but pick one canonical form and use it consistently.
- Use `pytorch` for framework-level posts; reserve `torch` only for narrowly torch-specific API discussions if needed.
- Prefer normalized technology names such as `postgresql`, `docker`, `pagefind`, `cuda`, `tensorrt`, `onnxruntime`.
- Use `visual-studio-code`, not `visual-code`.

### Tag Conflict Policy

- Avoid synonymous duplicates on the same post.
- Avoid plural/singular duplicates unless they have distinct meanings.
- Avoid both broad and needlessly redundant variants when one tag is enough.
- Do not use `paper-review` or category names as tags.

Examples:

- Prefer `proxy` over both `proxy` and `corporate-proxy` unless both meanings are needed.
- Prefer `cuda` plus `cudnn` when both are relevant, but do not add near-duplicates for version naming unless the post is specifically about version compatibility.

## Rollout Policy

- Apply categories to all posts first.
- Rebuild tags from scratch after categories are in place.
- When in doubt, choose the smaller taxonomy footprint.
