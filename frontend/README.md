# MyUs Frontend

React + [TanStack Router](https://tanstack.com/router) + [TanStack Query](https://tanstack.com/query) + [Vite](https://vite.dev/)

## 開発

```bash
pnpm install
cp .env.sample .env.local  # 値を設定する
pnpm dev                   # http://127.0.0.1:3000
```

## コマンド

| コマンド | 内容 |
|------|------|
| `pnpm dev` | 開発サーバーを起動 |
| `pnpm build` | lint の後に本番用にビルド（`dist/`） |
| `pnpm start` | ビルド結果をプレビュー |
| `pnpm test` | テスト（Vitest） |
| `pnpm lint` | ESLint |

## 環境変数

`VITE_` で始まる変数だけがブラウザに公開される。読み込むのは `src/lib/config.ts` のみ。

`vite build`（本番モード）では `.env.production` が `.env.local` より優先される。手元で `.env.local` の値を使ってビルドする場合は `vite build --mode development` を使う。

## ルーティング

URL とページの対応は `src/lib/routes.tsx` にまとめている。詳細は `docs/frontend.md` を参照。
