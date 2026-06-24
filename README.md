# migrate_myblog

Hugo 기반 블로그 소스 저장소입니다. 실제 사이트 소스는 `site/` 아래에 있으며, 배포는 GitHub Pages용 GitHub Actions 워크플로로 처리합니다.

- 프로덕션 URL: `https://chadrick-kwag.github.io/`
- Hugo 설정 파일: `site/hugo.yaml`
- GitHub Pages 워크플로: `.github/workflows/hugo.yaml`

## 디렉토리 구조

주요 디렉토리와 파일만 보면 아래와 같습니다.

```text
.
├── .github/
│   └── workflows/
│       └── hugo.yaml
├── docs/
├── site/
│   ├── content/
│   │   ├── _index.md
│   │   ├── archives.md
│   │   ├── search.md
│   │   └── posts/
│   │       └── <slug>/
│   │           ├── index.md
│   │           └── images/
│   ├── layouts/
│   ├── hugo.yaml
│   ├── go.mod
│   └── public/
├── tests/
├── tools/
└── AGENTS.md
```

설명:

- `site/content/`: 블로그 콘텐츠 본문
- `site/content/posts/`: 개별 포스트 페이지 번들 위치
- `site/layouts/`: Hugo 레이아웃 오버라이드
- `site/hugo.yaml`: 사이트 기본 설정과 메뉴, permalink, baseURL
- `.github/workflows/hugo.yaml`: GitHub Pages 빌드/배포 설정
- `site/public/`: Hugo 빌드 결과물 디렉토리로, 커밋 대상이 아님

## 포스트 구조

이 저장소는 Hugo page bundle 구조를 기준으로 사용합니다.

```text
site/content/posts/<slug>/
├── index.md
└── images/
    └── example.png
```

본문에서는 상대 경로 이미지 참조를 사용합니다.

```md
![](images/example.png)
```

## 로컬에서 Hugo 서버 띄우기

저장소 루트에서 아래 명령으로 개발 서버를 실행합니다.

```bash
.tools/bin/hugo server --source site --buildDrafts
```

기본 접속 주소:

- `http://localhost:1313/`

설명:

- `--source site`: Hugo 사이트 루트를 `site/`로 지정
- `--buildDrafts`: `draft: true` 글도 함께 렌더링

## 로컬 빌드

배포 전 확인용 프로덕션 스타일 빌드는 아래 명령을 사용합니다.

```bash
rm -rf site/public
.tools/bin/hugo --source site --panicOnWarning --minify
```

변경 후 권장 확인 명령:

```bash
git diff --check
git status --short
```

## GitHub Pages 배포 정보

이 저장소는 GitHub Pages 사용자 사이트로 배포됩니다.

- 대상 저장소: `chadrick-kwag.github.io`
- 기본 브랜치: `main`
- 배포 트리거: `main` 브랜치 push, 또는 수동 실행

워크플로 동작 요약:

1. GitHub Actions가 저장소를 checkout
2. Hugo Extended, Go, Node.js, Dart Sass 설치
3. `hugo --source site`로 사이트 빌드
4. GitHub Pages가 제공하는 `base_url`을 빌드 시 주입
5. 생성된 `site/public`을 artifact로 업로드
6. `actions/deploy-pages`로 Pages 배포

현재 Hugo 설정의 기본 `baseURL`은 아래 값으로 유지해야 합니다.

```yaml
baseURL: https://chadrick-kwag.github.io/
```

## 주의사항

- `site/public/`은 생성 산출물이므로 커밋하지 않습니다.
- 일반적인 블로그 작업은 주로 `site/content/**`, `site/hugo.yaml`, `.github/workflows/hugo.yaml` 범위에서 수행합니다.
- 카테고리와 태그 규칙은 `docs/blog-taxonomy-guidelines.md`를 따릅니다.
