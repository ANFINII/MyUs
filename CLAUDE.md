# Claude Code 開発ルール

## コーディングルール

コードを書いた後、必ず対象のルールファイルを**読み込んで**確認し、ルールに適合しているか検証すること。

### バックエンド（myus/）
- ルールファイル: [docs/backend.md](docs/backend.md)
- 対象: Python/Djangoコード
- 確認後: `uv run mypy myus config tests` と `uv run ruff check myus config tests --extend-ignore I` でリンターチェックを実行（ruff の `I`（import の並べ替え）は `docs/backend.md` の import の決まりと合わないため除く）

### フロントエンド（frontend/）
- ルールファイル: [docs/frontend.md](docs/frontend.md)
- CSS/SCSS: [docs/css.md](docs/css.md)
- 対象: TypeScript/React（Vite + TanStack Router）コード
- 確認後: `pnpm check` でリンター・型チェックを実行

## 確認フロー

1. コードを書く
2. 対象のルールファイルをReadツールで読み込む
3. ルールに適合しているか確認し、違反があれば修正
4. リンターチェック（BE: `uv run mypy`、FE: `pnpm check`）を実行してエラーがあれば修正
