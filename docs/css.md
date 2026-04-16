# SCSS コーディングルール

## 基本原則

- ファイル形式は必ずSCSSを使用
- `parts/`、`widgets/`はCSS Modules（`.module.scss`）を使用
- `templates/`ではグローバルCSS（`styles/`配下）を利用してよい
- ネスト構文で記述する（子要素は親クラスの中にネスト、3階層まで）
- インラインスタイルは使用しない
- 動的スタイルはクラスの切り替え（`cx()`）で対応

## 命名規則

- クラス名: `snake_case`
- ファイル名: `ComponentName.module.scss`（PascalCase）

## プロパティ記述順序

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
  background: rgb(245, 245, 245);
  border: 1px solid rgb(220, 220, 220);
  border-radius: 5px;

  // 5. その他
  cursor: pointer;
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
