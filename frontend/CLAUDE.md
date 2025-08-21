# Claude Code フロントエンド開発ルール

## 基本原則

### 1. TypeScript厳格モード
- **絶対にany型を使用しない**
- すべての変数、関数の引数、戻り値に適切な型を定義する
- 型推論が効く場合でも、複雑な型は明示的に定義する

### 2. エラーハンドリング
- `undefined`や`null`の可能性がある場合は必ずチェックする
- オプショナルチェーン（`?.`）や Nullish Coalescing（`??`）を活用
- try-catchブロックではエラーを適切に処理し、console.logは使用しない

### 3. React/Next.js規約
- 関数コンポーネントを使用（クラスコンポーネントは使用しない）
- カスタムフックは`use`プレフィックスを付ける
- コンポーネント名はPascalCase、その他の関数はcamelCase

## コーディング規約

### インポート順序
```typescript
1. React関連
2. 外部ライブラリ
3. 内部型定義
4. 内部コンポーネント
5. スタイル
```

### 命名規則
- **Props型**: `Props`または`${ComponentName}Props`
- **状態変数**: `[value, setValue]`の形式
- **イベントハンドラー**: `handle${EventName}`の形式
- **boolean変数**: `is${State}`、`has${Feature}`、`should${Action}`

### スタイル
- **必ずCSS Modulesを使用**（`.module.scss`）
- **インラインスタイルは絶対に使用しない**
- **すべてのスタイルはクラスを定義してSCSSファイルに記載**
- 既存のクラスを優先的に使用
- 動的なスタイルが必要な場合も、可能な限りクラスの切り替えで対応

## 品質管理

### ESLint/Prettier遵守
- すべてのESLintエラーを解決
- ファイル末尾に改行を追加
- セミコロンなし（設定による）
- トレーリングカンマを使用

### 型安全性
```typescript
// ❌ 悪い例
const playerRef = useRef<any>(null)
const handleClick = (e: any) => {}

// ✅ 良い例
type Player = ReturnType<typeof videojs>
const playerRef = useRef<Player | null>(null)
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {}
```

### Null/Undefinedチェック
```typescript
// ❌ 悪い例
playerRef.current.play()

// ✅ 良い例
if (playerRef.current && playerRef.current.play) {
  playerRef.current.play()
}
// または
playerRef.current?.play?.()
```

## スタイル記述の例

### ❌ 悪い例
```tsx
<div style={{ width: 272, height: 153, display: 'block' }}>
  <img style={{ objectFit: 'cover' }} />
</div>
```

### ✅ 良い例
```tsx
// Component.tsx
<div className={styles.videoContainer}>
  <img className={styles.thumbnail} />
</div>

// Component.module.scss
.videoContainer {
  width: 272px;
  height: 153px;
  display: block;
}

.thumbnail {
  object-fit: cover;
}
```

### 動的スタイルの扱い
```tsx
// ❌ 悪い例
<div style={{ display: isHovered ? 'block' : 'none' }}>

// ✅ 良い例
<div className={cx(styles.content, { [styles.visible]: isHovered })}>
// または
<div className={isHovered ? styles.contentVisible : styles.contentHidden}>
```

## プロジェクト固有ルール

### video.js使用時
- Player型は`ReturnType<typeof videojs>`を使用
- `any`型の代わりに適切な型定義を探す
- プレーヤーの存在確認を必ず行う

### Media関連コンポーネント
- 既存のスタイルを活用
- デザインシステムを崩さない
- レスポンシブデザインを考慮

### パフォーマンス
- 不要な再レンダリングを避ける（useCallback、useMemoの適切な使用）
- 大きなコンポーネントは適切に分割
- 画像は適切なサイズと形式を使用

## デバッグとエラー処理

### console使用禁止
```typescript
// ❌ 悪い例
console.log('Error:', error)

// ✅ 良い例
// エラーはサイレントに処理するか、適切なエラーハンドリングを実装
.catch(() => {
  // Handle error silently or show user-friendly message
})
```

### 開発時の確認事項
1. TypeScriptエラーが0件であること
2. ESLintエラーが0件であること
3. ビルドが成功すること
4. 実行時エラーがないこと
5. コメントアウトは日本語であること

## コンポーネント作成チェックリスト

- [ ] TypeScript型定義が完全
- [ ] any型を使用していない
- [ ] Propsインターフェースを定義
- [ ] エラーハンドリングを実装
- [ ] ESLintエラーなし
- [ ] 既存のスタイルを活用
- [ ] レスポンシブ対応
- [ ] パフォーマンス最適化

## 更新履歴
- 2024-08-21: 初版作成