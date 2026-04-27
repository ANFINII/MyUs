# フロントエンド開発ルール

## TypeScript

- any型は使用しない
- すべての関数の引数・戻り値に型を定義する
- `undefined`/`null`の可能性がある値は`?.`や`??`でチェックする
- console.logは使用しない（エラーはサイレント処理またはUI通知）

## React/Next.js

- 関数コンポーネントのみ使用
- コンポーネント名はPascalCase、関数はcamelCase
- カスタムフックは`use`プレフィックス
- Propsは分割代入せず`props`で受け取り、内部で展開する
- `interface Props`は`export default function`の直前に定義する（コンポーネントのシグネチャと型定義が視覚的に隣接するように）

```typescript
interface Props {
  value: string
  onChange: (value: string) => void
}

export default function Component(props: Props): React.JSX.Element {
  const { value, onChange } = props
}
```

他の型定義（ユニオン型・補助型など）は`interface Props`より上に書く。

```typescript
type AlertType = 'info' | 'warning' | 'error'

const iconMap = {
  info: IconInfo,
  warning: IconWarning,
  error: IconError,
}

interface Props {
  type?: AlertType
  children: React.ReactNode
}

export default function Alert(props: Props): React.JSX.Element {
  // ...
}
```

## 命名規則

| 対象 | 規則 | 例 |
|------|------|-----|
| Props型 | `Props`のみ | `interface Props {}` |
| 状態変数 | `[value, setValue]` | `[count, setCount]` |
| イベントハンドラー | `handle${Event}` | `handleSubmit` |
| boolean変数 | `is${State}` | `isLoading`, `isOpen` |

## useState

- 必ず型引数を指定する

```typescript
const [count, setCount] = useState<number>(0)
const [name, setName] = useState<string>('')
const [items, setItems] = useState<Item[]>([])
const [user, setUser] = useState<User | null>(null)
```

## インポート順序

```
1. React関連
2. 外部ライブラリ
3. 内部型定義
4. 内部コンポーネント
5. スタイル
```

## 非同期処理

- API呼び出しは`async/await`で記述する
- エラーハンドリングは`Result`型（`isErr()`）パターンで行う
- ローディング状態は`useIsLoading`フックで管理する

## コンポーネント設計

- 1ファイル1コンポーネント（default export）
- ロジックが複雑になったらカスタムフックに切り出す
- `pages/`はデータ取得（`getServerSideProps`等）とテンプレート呼び出しのみ
- `templates/`にページの実装を置く

## ディレクトリ構成の責務

| ディレクトリ | 責務 |
|------|------|
| `pages/` | ルーティング、SSRデータ取得 |
| `templates/` | ページの実装、状態管理 |
| `widgets/` | 複合コンポーネント（Modal, Card等） |
| `parts/` | 汎用UIコンポーネント（Button, Input等） |
| `hooks/` | カスタムフック |
| `api/` | APIクライアント関数 |
| `types/` | 型定義 |
| `utils/` | ユーティリティ関数 |

## 依存方向

`parts/` ← `widgets/` ← `templates/` ← `pages/` の片方向のみ依存する。逆方向や同階層への依存は禁止。

### parts は独立性を持つ

- `parts/` 配下のコンポーネントは他の `parts/` を import しない（最下層UIとしてそれ単体で動作する）
- レイアウト（縦並び・間隔等）は `VStack` / `HStack` などの parts に頼らず、自前の `<div>` + CSS（`display: flex` / `gap` 等）で実現する
- `widgets/` / `templates/` から parts を呼ぶ・複数 parts を組み合わせるのは正常な使い方

```typescript
// ❌ NG: parts/Input が他 parts に依存
import VStack from 'components/parts/Stack/Vertical'
return <VStack gap="2">...</VStack>

// ✅ OK: 自前の div + CSS
return <div className={style.box}>...</div>
// .box { display: flex; flex-direction: column; gap: 4px; }
```

#### 例外として許容されるケース

以下のパターンは「parts → parts」依存でも例外として許容する。レビュー時の判断基準にする。

1. **純粋表示用 parts への依存**: `Icon` / `Spinner` / `ExImage` 等、state を持たず描画だけする parts は他 parts から import してよい
2. **同ファミリ内の派生**: `Avatar/Link` が `Avatar` を呼ぶ、`Button/Square` が `Button` の補助 parts を共有する等、同コンポーネントファミリのサブバリアント
3. **同サブツリーのプリミティブ取り込み**: `Input/SelectBox` が `Input/Select` を内部で使う等、同フォルダ階層の下位 parts への限定依存
4. **合成 UI として例外的に parts に置く部品**: `Modal` のような汎用合成 UI で、内部にクローズ用 `Button` 等の小さな部品を含むケース（移動候補ではあるが許容）

判定は「循環依存を作らないか」「最下層 UI の独立性を本質的に壊さないか」を基準にする。

### parts の CSS も独立性を持つ

- `parts/` の `.module.scss` はグローバル CSS や共有 mixin / 変数に依存しない（その scss 単体で完結する）
- `styles/` 配下の `@use` / `@import` を行わない、`:global(...)` も使わない、`className="text_sub"` 等のグローバルユーティリティクラスを使用しない
- 必要な値（色・サイズ等）はその場で `rgb(...)` や `px` を直接記述する
- 例外: SCSS の標準モジュール（`@use 'sass:math'` 等）はビルトインなので使用可
- `widgets/` / `templates/` ではグローバル CSS / 共有 mixin の利用を許容（ページ単位の構成のため）

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

## スタイル

[SCSSコーディングルール](css.md) を参照。

## リンターチェック（必須）

コードを書いた後、必ず `npm run lint` を実行する。

### 確認事項
1. TypeScriptエラーが0件
2. ESLintエラーが0件
3. コメントは日本語で記述

## 更新履歴
- 2024-08-21: 初版作成
- 2025-08-21: Props名統一、引数展開ルール、Linterチェック必須化
- 2026-04-16: useState型引数必須、docs/に一元化、構成整理
- 2026-04-22: `interface Props`はコンポーネント関数の直前配置ルール追加
- 2026-04-27: 依存方向ルール追加（`parts/` は他 parts / グローバル CSS に依存せず単体で動作する）
- 2026-04-27: parts 独立性の例外ケース 4 種を明文化（純粋表示用・同ファミリ派生・同サブツリー・汎用合成 UI）
