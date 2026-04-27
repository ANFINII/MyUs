# SCSS コーディングルール

## 基本原則

- ファイル形式は必ずSCSSを使用
- `parts/`、`widgets/`はCSS Modules（`.module.scss`）を使用
- `templates/`ではグローバルCSS（`styles/`配下）を利用してよい
- ネスト構文で記述する（子要素は親クラスの中にネスト、3階層まで）
- インラインスタイルは使用しない
- 動的スタイルはクラスの切り替え（`cx()`）で対応

## parts の SCSS 独立性（必須）

`parts/` の `.module.scss` はそれ単体で完結させる。グローバル CSS / 共有 mixin / 共有変数に依存しない。

- `@use 'styles/...'` / `@import 'styles/...'` を書かない
- `:global(.foo)` を使わない
- `className="text_sub"` 等のグローバルユーティリティクラスを参照する前提のスタイルを書かない
- 必要な値（色・サイズ等）は `rgb(...)` / `px` 直書き
- 例外: SCSS ビルトイン（`@use 'sass:math'` 等）は OK

`widgets/` / `templates/` ではグローバル CSS / 共有 mixin の利用を許容（ページ単位の構成のため）。

詳細とコード例は [docs/frontend.md の「依存方向」](frontend.md#依存方向) を参照。

## 命名規則

- クラス名: `snake_case`
- ファイル名: `ComponentName.module.scss`（PascalCase）

## プロパティ記述順序

以下の順でプロパティを並べる。分類コメント（`// 1. レイアウト` 等）はこのドキュメント上での参照用であり、**実際のSCSSファイルには記述しない**。

```scss
.element {
  // 1. レイアウト
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  // 2. ボックスモデル
  width: 100px;
  padding: 4px 8px;
  margin: 0;
  // 3. テキスト
  font-size: 13px;
  text-align: left;
  white-space: nowrap;
  color: rgb(80, 80, 80);
  // 4. 装飾
  border: 1px solid rgb(220, 220, 220);
  border-radius: 5px;
  background: rgb(245, 245, 245);
  // 5. その他
  cursor: pointer;
}
```

## 空行ルール

- **同一セレクタ内のプロパティ間は空行を入れない**
- **異なるセレクタ（ネスト含む）の間は空行を1行入れる**

実ファイルの例（分類コメントなし、セレクタ間のみ空行あり）:

```scss
.alert {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 10px 12px;
  font-size: 13px;
  border: 1px solid transparent;
  border-radius: 5px;

  &.info {
    color: rgb(30, 90, 180);
    border-color: rgb(200, 220, 250);
    background: rgb(235, 245, 255);
  }

  &.warning {
    color: rgb(150, 100, 10);
    border-color: rgb(240, 210, 120);
    background: rgb(255, 248, 225);
  }

  .icon {
    display: flex;
    align-items: center;
    flex-shrink: 0;
  }
}
```

## 値の記述

- 色: `rgb()`を使用（16進数・カラーネーム不可）
- 単位: `px`基本、`0`は単位省略
- 共通プロパティは複数セレクタをカンマ区切りでまとめる

## 詳細度

- `!important`は使用しない
- 上書きが必要な場合はセレクタを重ねる: `.align_right.align_right`
- CSS Modulesの読み込み順に依存しないよう、汎用コンポーネント側にユーティリティクラスを用意する

## レスポンシブ

- メディアクエリはコンポーネント単位でSCSSファイル内に記述
- モバイルファーストで`min-width`で拡張

## 更新履歴
- 2026-04-16: 初版作成
- 2026-04-22: 空行ルール追加（同一セレクタ内は詰める、セレクタ間は改行）、分類コメントは実ファイルに書かない旨を明記
- 2026-04-27: parts の SCSS 独立性ルール追加（グローバル CSS / 共有 mixin に依存しない）
