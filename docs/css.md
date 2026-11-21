# SCSS コーディングルール

## 基本原則

- ファイル形式は必ずSCSSを使用
- `parts/`、`widgets/`はCSS Modules（`.module.scss`）を使用
- `pages/`ではグローバルCSS（`styles/`配下）を利用してよい
  - `styles/global/`：全体のスタイル（`reset.scss`・`style.scss` など）と mixin（`mixin/scrollbar.scss`・`mixin/tiptap.scss`）
    - ブログの本文の見た目は `tiptap.article` の1つにまとめる。入力画面の `TextEditor`、プレビューと詳細画面の `BlogArticle` の両方がこれを使い、書いている間と公開したあとの見た目をそろえる。チャットは `tiptap.tiptap` だけを使う
  - `styles/internal/`：特定の画面・ライブラリ向け（`registration.scss`・`videojs-myus.scss` など）
- ネスト構文で記述する。子要素は親クラスの中にネストし、5階層までにする。`&:hover`・`&.active` のように `&` で始まるものは階層に数えない
- インラインスタイルは使用しない。ただし、再生位置のバーの幅のように値が連続して変わるものだけは `style` で渡してよい
- 動的スタイルはクラスの切り替え（`cx()`。`utils/functions/cx.ts`）で対応
- 画面の幅は、画面ごとの SCSS に `max-width` を書かず、`layout/Main` の `size` で決める。`s` は380px、`m` は1020px、`l` は1280px

## parts の SCSS 独立性（必須）

`parts/` の `.module.scss` はそれ単体で完結させる。グローバル CSS / 共有 mixin / 共有変数に依存しない。

- `@use 'styles/...'` / `@import 'styles/...'` を書かない
- `:global(.foo)` を使わない
- `className="text_sub"` 等のグローバルユーティリティクラスを参照する前提のスタイルを書かない
- 必要な値（色・サイズ等）は `rgb(...)` / `px` 直書き
- 例外: SCSS ビルトイン（`@use 'sass:math'` 等）は OK

`widgets/` / `pages/` ではグローバル CSS / 共有 mixin の利用を許容する。ページ単位の構成のため。

```scss
/* ❌ NG: parts の scss がグローバルに依存 */
@use 'styles/global/mixin/tiptap';
.box {
  @include tiptap.tiptap;
}

/* ✅ OK: parts の scss は単体で完結 */
.box {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
```

## 命名規則

- クラス名: `snake_case`
- ファイル名: `ComponentName.module.scss`（PascalCase）

## プロパティ記述順序

以下の順でプロパティを並べる。分類コメント（`// 1. レイアウト` 等）はこのドキュメント上での参照用であり、**実際のSCSSファイルには記述しない**。

```scss
.element {
  // 1. レイアウト
  position: absolute;
  top: 0;
  left: 0;
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
  overflow-x: hidden;
  overflow-y: auto;
  transition: all 0.2s;
  z-index: 80;
  cursor: pointer;
}
```

MyUs でよく使うプロパティは、次の分類に入れる。同じ分類の中も、この表の順に並べる。

| 分類 | プロパティ |
| --- | --- |
| 1. レイアウト | `position`・`top`・`right`・`bottom`・`left`・`display`・`flex-direction`・`flex-wrap`・`justify-content`・`align-items`・`align-self`・`gap`・`flex`・`flex-shrink`・`grid-template-columns`・`grid-template-rows`・`grid-column`・`grid-row` |
| 2. ボックスモデル | `width`・`min-width`・`max-width`・`height`・`min-height`・`max-height`・`padding`・`margin`・`box-sizing`・`object-fit` |
| 3. テキスト | `font-family`・`font-size`・`font-weight`・`line-height`・`text-align`・`text-decoration`・`text-overflow`・`text-indent`・`white-space`・`word-break`・`overflow-wrap`・`list-style`・`color` |
| 4. 装飾 | `border`・`border-radius`・`outline`・`box-shadow`・`background` |
| 5. その他 | `overflow`・`overflow-x`・`overflow-y`・`opacity`・`transform`・`transition`・`animation`・`z-index`・`pointer-events`・`user-select`・`cursor` |

- `padding-top` や `border-bottom` のような一辺だけのものは、もとのプロパティと同じ分類に入れる
- `cursor` のような操作に関わるものは、どのセレクタでも一番下に書く
- 表にないプロパティは、近い役目のものと同じ分類に入れる

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
- デスクトップを基本にし、`max-width`で狭い画面向けに上書きする（例：`@media screen and (max-width: 668px)`）

