# Hugo S3 Blog Recovery Design

## Objective

Recover the published `chadrick-kwag.net` blog from its AWS S3 static output into a maintainable Hugo project. Preserve the articles and their assets in this repository now, then add GitHub Pages deployment after the GitHub username is chosen.

The target is a content-first recovery with a current Hugo theme. Pixel-identical reproduction of the old site is not a requirement.

## Confirmed Source State

- AWS account: `005073917867`
- Source bucket: `s3://chadrick-kwag.net` in `us-east-1`
- Published generator: Hugo `0.92.2`
- Published theme: `hugo-paper`
- Source inventory: 1,917 objects totaling 29,764,583 bytes
- Article inventory: 218 `posts/<slug>/index.html` pages. The broader 241
  `posts/**/index.html` count is 218 articles plus `posts/index.html` and 22
  pagination pages under `posts/page/`.
- Article images are generally stored below `posts/<slug>/images/`
- The bucket contains generated HTML and assets, but no Markdown, Hugo configuration, or original theme source.

## Scope

### Included

- Immutable local backup of all S3 objects
- Object manifest with sizes, ETags, and checksums where available
- Repeatable HTML-to-Hugo recovery tooling
- Recovery of titles, dates, modification dates, categories, tags, article bodies, links, code, tables, and images
- Hugo page bundles under `site/content/posts/<slug>/`
- Automated recovery and build validation
- A current, pinned PaperMod theme
- Repository boundaries that allow a later GitHub Actions deployment to GitHub Pages

### Excluded from the initial recovery

- Switching DNS or disabling AWS resources
- GitHub repository creation and GitHub Pages activation
- Custom domain configuration
- Advertising and analytics scripts
- Recreating the old Pagefind index
- Pixel-identical restoration of the old Paper theme

## Repository Structure

```text
migrate_myblog/
├── backup/s3/                    # Immutable byte-for-byte S3 download
├── manifests/                    # S3 inventory and backup verification data
├── tools/recover/                # Recovery command and focused conversion modules
├── tests/                        # Converter fixtures and behavior tests
├── reports/                      # Machine-readable recovery and validation results
├── site/
│   ├── content/posts/<slug>/
│   │   ├── index.md              # Recovered article and front matter
│   │   └── images/               # Article-local assets
│   ├── assets/                   # Site-owned processed assets
│   ├── static/                   # Unprocessed global assets
│   ├── layouts/                  # Minimal project-specific overrides
│   ├── hugo.yaml                 # Site configuration
│   ├── go.mod                    # Pinned Hugo theme module
│   └── go.sum
├── docs/                         # Design and execution documentation
└── .github/workflows/            # Added when GitHub identity is known
```

Generated `site/public/` output is ignored by Git. AWS credentials and `.env` files are never committed.

## Recovery Architecture

The process has three explicit layers:

1. **Source preservation:** Download every S3 object into `backup/s3/` without rewriting content or paths. Record the remote inventory before downloading and verify the local result afterward.
2. **Deterministic conversion:** Read only from the backup and generate a fresh Hugo tree. Re-running conversion replaces generated recovery output but never changes the backup.
3. **Independent validation:** Inspect the recovered content, asset references, and Hugo build. Validation produces reports and a non-zero exit status when acceptance criteria are not met.

Each article converts independently. A failure in one article is recorded without hiding the failure or corrupting other recovered articles.

## Article Conversion Rules

For each `posts/<slug>/index.html`:

- Use the directory name as the stable slug.
- Extract the title from structured metadata, falling back to the article heading.
- Extract `date` and `lastmod` from `article:published_time`, `article:modified_time`, or equivalent item properties.
- Recover categories and tags from article taxonomy links when present.
- Select the article content container and exclude navigation, header, footer, analytics, advertisements, and theme controls.
- Convert headings, paragraphs, emphasis, links, lists, block quotes, code blocks, tables, figures, and images to Markdown.
- Keep unsupported content as inline raw HTML rather than discarding it.
- Rewrite same-site absolute links to root-relative links.
- Rewrite article-local image links to page-bundle-relative paths.
- Copy article assets into the matching page bundle without recompression or renaming.
- Encode front matter as YAML with `title`, `date`, `lastmod`, `slug`, `categories`, `tags`, and `draft: false`.

The converter must be idempotent: identical backup input and tool version produce identical recovered files.

## Failure Handling and Reports

`reports/recovery.json` records one result per article:

- source path and slug
- output path
- extraction status
- source and recovered text lengths
- copied and missing asset references
- unsupported HTML elements retained
- warnings and fatal error details

Fatal article failures leave no partial `index.md`. Warnings preserve output but cause the article to appear in a review list. The recovery command exits unsuccessfully if any article has a fatal error or if recovered article counts differ from source counts.

## Theme and Hugo Configuration

Use the latest tested stable PaperMod release at implementation time and pin its exact module version in `go.mod` and `go.sum`. PaperMod is close to the prior Paper presentation while providing a maintained responsive layout, dark mode, code presentation, archives, and client-side search.

The initial Hugo configuration uses a non-production placeholder base URL and preserves `/posts/<slug>/` permalinks. The final `https://<username>.github.io/` base URL is applied only after the GitHub username and repository exist.

Theme overrides remain minimal so future theme updates are manageable. Pagefind, advertising, and analytics are not carried over during recovery.

## Validation and Acceptance Criteria

Automated validation must establish all of the following:

- The local backup contains 1,917 objects and matches the recorded source inventory.
- Exactly 218 article page bundles contain an `index.md`; validation uses
  `expected_count=218` and excludes the posts index and pagination pages.
- Every recovered article has a non-empty title, date, slug, and body.
- Every local image reference resolves to a file with non-zero size.
- Every root-relative internal article link resolves to recovered content or is explicitly reported for review.
- Hugo completes a production build with warnings treated as errors where supported.
- No AWS credential pattern or `.env` content is tracked by Git.
- Text-length comparison flags substantial source-to-recovery differences for review.
- Representative fixtures verify paragraphs, nested lists, fenced code, tables, external links, internal links, Unicode filenames, and retained raw HTML.

Manual review covers a sample of old and recent posts, image-heavy posts, code-heavy posts, and posts containing tables or non-ASCII assets.

## Future GitHub Pages Deployment

After a GitHub username is chosen, the repository can be named `<username>.github.io`. A GitHub Actions workflow will:

1. Check out the repository and pinned theme dependencies.
2. install the tested Hugo version.
3. Build with `site/` as the source and the final Pages URL as `baseURL`.
4. Upload only `site/public/` as the Pages artifact.
5. Deploy that artifact through GitHub Pages.

`backup/`, `tools/`, `tests/`, and `reports/` remain repository source files but are not included in the deployed Pages artifact.

## Security and Operational Boundaries

- `.env` and AWS credentials remain local and ignored.
- A pre-commit credential scan is required before the first remote push.
- This recovery performs read-only AWS operations.
- AWS S3, CloudFront, certificates, and DNS remain unchanged until the GitHub Pages result has been reviewed and a separate cutover is approved.
- Because the future repository is public, only already-public website content belongs in the committed backup and reports.
