# フロントエンド開発ルール

## TypeScript

- any型は使用しない
- すべての関数の引数・戻り値に型を定義する
- `undefined`/`null`の可能性がある値は`?.`や`??`でチェックする
- console.logは使用しない（エラーはサイレント処理またはUI通知）

## React

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
- ローディング状態は`useLoading`フックで管理する
- ページ表示時のデータ取得は「データ取得（TanStack Query）」に従う

## データ取得（TanStack Query）

ページ表示時のデータ取得は`getServerSideProps`ではなく、TanStack Queryの`useQuery`でクライアント側から行う。

### ページの構成

- URLとページの対応は`src/lib/routes.tsx`の1ファイルにまとめる（TanStack Routerのコードベースのルーティング）。ページを追加するときは、該当する領域に`page()`を1行追加する
- ルートは`pages/`のコンポーネントを`lazyRouteComponent`で読み込むだけにする（表示するときに読み込まれる）
- 英語版（`/en/...`）を同じルートで受けるため、各ページは言語のルート（`{-$locale}`）の子にする
- 動的なパスパラメータは`$ulid`のように`$`で始める

```typescript
// src/lib/routes.tsx
page('/manage/video', () => import('pages/manage/video')),
page('/manage/video/create', () => import('pages/manage/video/create')),
page('/manage/video/$ulid', () => import('pages/manage/video/[ulid]')),
```

- クエリは名前付きのオブジェクトを`const queries`に入れてから`QueryCheck`（`widgets/Status/QueryCheck`）に渡し、エラー → 取得中 → 表示を判定させる
- `QueryCheck`は、渡した名前のまま取得データをまとめて`children`の関数に渡す。名前をテンプレートのpropsに合わせ、`{...props}`で渡す
- `QueryCheck`の`children`は、データを使う場合は関数、使わない場合はJSXで渡す
- `QueryCheck`のpropsは`title` → `queries` → `fresh`の順に書く

```typescript
export default function ManageVideoEditPage(): React.JSX.Element {
  const router = useAppRouter()
  const ulid = String(router.query.ulid ?? '')

  const channels = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()) })
  const categories = useQuery({ queryKey: queryKeys.categories, queryFn: () => toQuery(getCategories()) })
  const data = useQuery({ queryKey: queryKeys.manageVideoDetail(ulid), queryFn: () => toQuery(getManageVideo(ulid)), enabled: router.isReady })
  const queries = { data, channels, categories }

  return (
    <QueryCheck title="Video" queries={queries} fresh>
      {(props) => <ManageVideoEdit {...props} />}
    </QueryCheck>
  )
}
```

### useQuery の書き方

- `queryFn`は`toQuery`（`lib/query/client`）でAPI関数を包む（`Result`型をthrowに変換し、`error`を`ApiError`型として扱うため）
- `queryKey`は`lib/query/keys.ts`の`queryKeys`に定義する（`invalidateQueries`で前方一致させるため、配列の先頭から粒度が細かくなるようにする）
- 1行で書く。180文字（`printWidth`）を超えるものはPrettierの折り返しに任せる
- `useQuery`の結果は`queries`のキー（テンプレートのprops名）と同じ名前の変数に入れ、`const queries = { data, channels }`のように省略記法で書く
- 補助的なクエリ（チャンネル一覧・カテゴリ一覧等）を先に、ページの主となるクエリを後に書く
- 連続する`useQuery`の間、および直後の`const queries`との間に空行を入れない

### 用途別のルール

| 用途 | ルール |
|------|------|
| 取得データを`useState`の初期値に使う（作成・編集フォーム） | `QueryCheck`に`fresh`を付ける（画面を開いた後の取得完了を待ち、古いキャッシュでフォームが初期化され、古い値で上書き保存されるのを防ぐ） |
| ページ送り・検索等で`queryKey`が変わる一覧 | `placeholderData: keepPreviousData`で前の表示を残す（画面全体がスピナーに切り替わるのを防ぐ） |
| 一覧・表示のみ | `fresh`は付けない（キャッシュを即表示し、最新が届いたら置き換わる） |

### キャッシュ

- `staleTime: 0`のため、ページを開くたびに最新を取得する。更新処理のたびに`invalidateQueries`を呼ぶ必要はない
- ログイン・ログアウト・退会時のキャッシュ削除は`UserProvider`とログイン画面で行っているため、個別のページでは不要
- 全ページがクライアント側取得（CSR）。投稿ごとのOGPは、ホスティング先が決まってからエッジ関数で差し込む予定

## コンポーネント設計

- 1ファイル1コンポーネント（default export）
- ロジックが複雑になったらカスタムフックに切り出す
- `pages/`はデータ取得（`useQuery`）とテンプレート呼び出しのみ
- `templates/`にページの実装を置く

## ディレクトリ構成の責務

| ディレクトリ | 責務 |
|------|------|
| `pages/` | データ取得（`useQuery`）とテンプレート呼び出し |
| `templates/` | ページの実装、状態管理 |
| `widgets/` | 複合コンポーネント（Modal, Card等） |
| `parts/` | 汎用UIコンポーネント（Button, Input等） |
| `hooks/` | カスタムフック |
| `api/` | APIクライアント関数 |
| `lib/routes.tsx` | URL とページの対応（TanStack Router のルート定義） |
| `lib/query/` | TanStack Queryの設定（`client.ts`）とクエリキー（`keys.ts`） |
| `types/` | 型定義 |
| `utils/` | ユーティリティ関数 |

## 依存方向

`parts/` ← `widgets/` ← `templates/` ← `pages/` の片方向のみ依存する。逆方向や同階層への依存は禁止。

ただし、`widgets/` 内の同じフォルダ（同ファミリ）内の依存は許容する（例: `Status/QueryCheck` が `Status/Check`・`Status/Loading` を使う）。

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
- 2026-10-06: データ取得（TanStack Query）のルール追加、`pages/` の責務を `useQuery` に更新、widgets 同フォルダ内の依存を許容、`useIsLoading` → `useLoading` に修正
- 2026-10-06: `QueryCheck` がクエリを名前付きオブジェクトで受け取る形に変更（`useFreshData` を廃止し `fresh` に統合）
- 2026-10-06: `useQuery` の結果を `queries` のキーと同じ名前の変数に入れるルールを追加
- 2026-10-06: 公開ページの CSR 化完了に伴い、`getServerSideProps` が残っている旨の記述を削除
- 2026-10-07: Next.js から TanStack Router + Vite に移行。`getStaticProps` / `getStaticPaths` の記述を削除し、`routes/` の説明を追加
- 2026-10-07: ルート定義をファイルベース（`src/routes/`）からコードベース（`src/lib/routes.tsx` の 1 ファイル）に変更
- 2026-10-07: 常に `true` だった `router.isReady` を削除
