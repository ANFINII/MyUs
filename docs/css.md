# CSS/SCSS コーディングルール

## 基本原則

- **必ずCSS Modulesを使用**（`.module.scss`）
- **インラインスタイルは絶対に使用しない**
- **すべてのスタイルはクラスを定義してSCSSファイルに記載**
- 既存のクラスを優先的に使用
- 動的なスタイルが必要な場合も、可能な限りクラスの切り替えで対応

---

## 命名規則

### クラス名
- **snake_case**を使用（camelCaseやkebab-caseは使用しない）

```scss
// ❌ 悪い例
.videoContainer {}
.video-container {}

// ✅ 良い例
.video_container {}
```

### ファイル名
- コンポーネント名に合わせたPascalCase: `ComponentName.module.scss`

---

## 構造

### ネスト
- **子要素のクラスは親クラスの中にネストして定義する**
- ネストは3階層までを目安とする

```scss
// ❌ 悪い例（フラットに定義）
.container {
  min-height: 94px;
}

.heading {
  font-size: 16px;
}

.article {
  display: block;
}

// ✅ 良い例（親クラスの中にネスト）
.container {
  min-height: 94px;

  .heading {
    font-size: 16px;
  }

  .article {
    display: block;
  }
}
```

### 共通スタイルのグループ化
- 複数セレクタに共通するプロパティはカンマ区切りでまとめる

```scss
// ❌ 悪い例
.th {
  padding: 4px 8px;
  vertical-align: middle;
}

.td {
  padding: 4px 8px;
  vertical-align: middle;
}

// ✅ 良い例
.th,
.td {
  padding: 4px 8px;
  vertical-align: middle;
}
```

---

## 詳細度

### `!important`は使用しない
- 詳細度の問題はセレクタの構造で解決する

### 詳細度を上げる場合
- 同じクラスを重ねて詳細度を上げる（`.class.class`パターン）

```scss
// 通常の定義
.th {
  text-align: left;
}

// 上書きが必要な場合（詳細度を上げる）
.align_right.align_right {
  text-align: right;
}
```

### CSS Modulesの読み込み順に依存しない
- 外部コンポーネントのクラスを上書きする場合、読み込み順で負けることがある
- 汎用コンポーネント側にalignやサイズ用のクラスを用意して対応する

---

## プロパティ記述順序

以下の順序でプロパティを記述する:

```scss
.element {
  // 1. レイアウト
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;

  // 2. ボックスモデル
  width: 100px;
  min-width: 100px;
  max-width: 100px;
  padding: 4px 8px;
  margin: 0;

  // 3. テキスト
  font-size: 13px;
  font-weight: 500;
  text-align: left;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
  color: rgb(80, 80, 80);

  // 4. 装飾
  background: rgb(245, 245, 245);
  border: 1px solid rgb(220, 220, 220);
  border-radius: 5px;

  // 5. その他
  cursor: pointer;
  vertical-align: middle;
}
```

---

## 値の記述

### 色
- **`rgb()`を使用**（16進数やカラーネームは使用しない）

```scss
// ❌ 悪い例
color: #333;
color: gray;

// ✅ 良い例
color: rgb(51, 51, 51);
color: rgb(128, 128, 128);
```

### 単位
- `0`の場合は単位を省略: `margin: 0`
- `px`を基本単位として使用
- フォントサイズは`px`を使用

### マジックナンバー
- 繰り返し使う値はSCSS変数にする検討をする
- ただし1箇所でしか使わない値は直接記述してよい

---

## 動的スタイル

### クラスの切り替えで対応
```tsx
// ❌ 悪い例
<div style={{ display: isVisible ? 'block' : 'none' }}>

// ✅ 良い例
<div className={cx(styles.content, { [styles.visible]: isVisible })}>
// または
<div className={isVisible ? styles.visible : styles.hidden}>
```

### 条件付きクラスの結合
- `cx()`ユーティリティを使用してクラスを結合する

```tsx
<th className={cx(style.th, column.className, column.headerClass)}>
```

---

## レスポンシブ

- メディアクエリはコンポーネント単位でSCSSファイル内に記述
- モバイルファーストで記述し、`min-width`で拡張

---

## 更新履歴
- 2026-04-16: 初版作成
