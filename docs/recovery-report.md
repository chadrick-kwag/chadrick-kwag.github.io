## Hugo recovery verification report

Date: 2026-06-21

- S3 manifest: bucket `chadrick-kwag.net`, object_count `1917`, total_size `29764583`
- Recovery report: source_count `218`, success_count `218`, failure_count `0`, warning_count `0`
- Validation: `true` (`reports/validation.json`)
- Hugo: `v0.163.3-4d22555aebf458d5d150500c9ac4bee5b24cf0d3+extended`
- Theme baseline: PaperMod commit `a2eb47bb4b805116dcd34c1605d39835121f8dbe`
- Verification status: pytest passed (`137 passed`), Hugo build passed, recovery validation passed, `git diff --check` passed
- Credential checks: secret pattern scan returned no matches; `.env` is ignored by `.gitignore`; `.env` is not tracked
- Manual review sample slugs: `nginx-configuration-confusion-due-to-wordpress` (oldest), `cv2-resize-interpolation-methods`, `densenet-paper-review`, `focal-loss-a-k-a-retinanet-paper-review`, `adding-adsense-and-google-analytics-to-hugo` (newest)
- Content spot-check: sampled posts have valid front matter, plausible Markdown structure, working-looking headings/code blocks/lists/images, and date ordering consistent with oldest/newest sample
- AWS operations note: verification used read-only manifest/report inspection only; no AWS state was modified
