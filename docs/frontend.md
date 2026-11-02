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

ページ表示時のデータ取得は`getServerSideProps`ではなく、TanStack Queryの`useSuspenseQuery`でクライアント側から行う。

### ページの構成

- URLとページの対応は`src/lib/routes.tsx`の1ファイルにまとめる（TanStack Routerのコードベースのルーティング）。ページを追加するときは、該当する領域に`page()`を1行追加する
- ルートは`components/pages/`のページのフォルダ（`index.tsx`）を`lazyRouteComponent`で読み込むだけにする（表示するときに読み込まれる）
- ルーターの機能は `useRouter`（`components/hooks/useRouter`）を通して使う。使い方は Next.js の `useRouter` と同じにしている。コンポーネントから `@tanstack/react-router` や `window.location` / `window.history` を直接使わない（ルーターのライブラリを置き換えるときに、`useRouter` とルーターの設定だけを直せばよいようにするため）

| やりたいこと | 書き方 |
| --- | --- |
| 画面遷移 | `` router.push(`/media/video/${ulid}`) `` |
| クエリ文字列付きの画面遷移 | `router.push({ pathname: '/media/video', query: { search: name } })` |
| 今のページのクエリ文字列だけ変える | `router.push({ pathname: router.pathname, query: { ...router.query, page: 2 } })` |
| 履歴に残さない画面遷移 | `router.replace('/')` |
| 外部 URL への遷移 | `router.push('https://...')` |
| URL のパラメータ・クエリ文字列（`$ulid`、`?search=`） | `router.query.ulid`、`router.query.search`。文字列にするときは `String(router.query.ulid ?? '')` と書く（`?.toString()` は使わない。`String(router.query.ulid)` だけだと、無いときに `'undefined'` になる） |
| 今のパス（言語の接頭辞は含まない） / 表示中の言語 | `router.pathname` / `router.locale` |
| 戻る・再読み込み | `router.back()`・`router.reload()` |
| 戻れる履歴があるか（Next.js にはない） | `router.canBack()` |
| 表示中の言語を付けた絶対 URL（Next.js にはない） | `router.buildUrl('/media/chat/...')` |

- 英語版（`/en/...`）は、ルーターの `rewrite`（`src/lib/router.ts`）で URL の先頭の言語を取り除いてからルートに当てる。画面遷移では言語を付けずにパスを書けば、表示中の言語が自動で付く
- 動的なパスパラメータは`$ulid`のように`$`で始める

```typescript
// src/lib/routes.tsx
page('/manage/video', () => import('components/pages/manage/video')),
page('/manage/video/create', () => import('components/pages/manage/video/create')),
page('/manage/video/$ulid', () => import('components/pages/manage/video/edit')),
```

- ページの`index.tsx`は、`useSuspenseQuery(xxxQuery(...))`で取ったデータを`view.tsx`にpropsで渡すだけにする。データが取れるまで描画を待つので、`data`が`undefined`になる場合を書かなくてよい
- 取得中の表示はrouterの`defaultPendingComponent`（`Status/Loading`の`PageLoading`）、エラーの表示は`defaultErrorComponent`（`Status/RouteError`）に任せる。ページごとに取得中・エラーを判定しない
- ページ遷移の前にデータを取るルートは、`lib/query/options.ts`の`queryOptions`（`refetchOnMount: false`を含める）を、`lib/query/loaders.ts`の`xxxLoader`（`queryClient.query(xxxQuery(...))`）とページの`useSuspenseQuery(xxxQuery(...))`で共有し、`lib/routes.tsx`では`page('/path', () => import(...), xxxLoader)`の1行で登録する
  - 取得が終わるまで前のページを表示したまま、ヘッダーのバーで待つ（何秒かかっても画面全体のスピナーは出さない。最初にサイトを開いたときだけ、1秒を超えると`PageLoading`を出す。`PageLoading`は、まだ1ページも表示していないときだけスピナーを出す）
  - ローダーは取得の失敗を握りつぶさない（`.catch(noop)`を付けない）。失敗するとルートのエラー表示になる。握りつぶすと、ページの`useSuspenseQuery`が同じリクエストをもう一度送るため（`prefetchQuery`・`fetchQuery`・`ensureQueryData`は非推奨のため使わない）
  - 表示を待たないデータ（ユーザーページの投稿・広告など、後から出すもの）だけは、ページで`useQuery`を使い、ローダーでは`.catch(noop)`で握りつぶす
  - 閲覧数の加算など、遷移のたびに1回だけ行う処理は`queryFn`ではなく`xxxLoader`の中で呼ぶ（`queryFn`は再試行で複数回呼ばれる）
  - チャットのスレッド（`/media/chat/$ulid/thread/$messageUlid`）は`chatThreadLoader`で詳細だけを取り、閲覧数は加算しない（加算はチャットの`chatDetailLoader`だけ）
- エラー時の画面は`Status/RouteError`（中で`Status/Check`）が`ApiError.type`（BEの`ErrorOut.type`）で出し分ける。`status`を見るのは、500画面の判定（nginx等が返したエラー・ネットワークエラーは`type`を持たない）と再試行（`shouldRetry`）だけにする
- ログインしているかを確かめるだけのページは、`useSuspenseQuery(userQuery())`を呼ぶだけにする（ログインしていなければ401の画面になる）

```typescript
export default function ManageVideoEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const { data: channels } = useSuspenseQuery(channelsQuery())
  const { data: categories } = useSuspenseQuery(categoriesQuery())
  const { data } = useSuspenseQuery(manageVideoQuery(ulid))

  return <ManageVideoEdit channels={channels} categories={categories} data={data} />
}
```

### useSuspenseQuery の書き方

- `queryFn`は`toQuery`（`lib/query/client`）でAPI関数を包む（`Result`型をthrowに変換し、`error`を`ApiError`型として扱うため）
- `queryKey`は`lib/query/keys.ts`の`queryKeys`に定義する（`invalidateQueries`で前方一致させるため、配列の先頭から粒度が細かくなるようにする）
- `queryKeys`と`queryOptions`の名前は、取得関数（`getVideos`・`getVideo`）に合わせて一覧を複数形（`manageVideos`・`manageVideosQuery`）、詳細を単数形（`manageVideo`・`manageVideoQuery`）にする。一覧と詳細をまとめて`invalidateQueries`するキーは`All`を付ける（`manageVideoAll`）
- 1行で書く。180文字（`printWidth`）を超えるものはPrettierの折り返しに任せる
- `useSuspenseQuery`の結果は`const { data: channels } = ...`のように、`view.tsx`のprops名と同じ名前の変数に入れる
- 一覧・詳細・編集ページの主となるクエリは`data`と名付ける（`datas`・`mediaHome`のような個別の名前にしない）
- 主となるクエリが無いページ（作成画面）や、複数の種類のデータを並べて扱うページ（設定画面・ユーザーページ等）は、扱うものの名前を付ける（`channels`・`categories`・`mypage`・`profile`・`user`・`userPage`等）
- 補助的なクエリ（チャンネル一覧・カテゴリ一覧等）を先に、ページの主となるクエリを後に書く
- `index.tsx`の関数の中は、`return`の前に空行を入れる。`router`・`params`などの準備と`useSuspenseQuery`の間には空行を入れない。ただし`useSuspenseQuery`が2行以上続くとき、または`useSuspenseQuery`の結果を使って次の`useSuspenseQuery`の引数を作るとき（管理画面の一覧の`channels` → `channel`・`params` → `data`）は、そのまとまりの上に空行を入れてよい（まとまりの中には入れない）
- `view.tsx`に渡すpropsは、`useSuspenseQuery`で取ったものを書いた順（補助的なもの → 主となる`data`）に先に並べ、そのあとに`page`・`ulid`などURLから作った値を並べる（例: `channels` → `data` → `page`）
- `view.tsx`の`interface Props`と`const { ... } = props`も、`index.tsx`で渡す順に並べる

### 用途別のルール

| 用途 | ルール |
|------|------|
| 取得データを`useState`の初期値に使う（作成・編集フォーム） | そのまま使う（`loader`が遷移のたびに最新を取ってから表示するため、古いキャッシュでフォームが初期化されない） |
| ページ送り・検索等で`queryKey`が変わる一覧 | `keepPreviousData`は使わない（URLのクエリが変わると`loader`が動き、前のページを表示したまま待つ） |

### キャッシュ

- `staleTime: 0`のため、ページを開くたびに最新を取得する。更新処理のたびに`invalidateQueries`を呼ぶ必要はない
- ログイン・ログアウト・退会時のキャッシュ削除は`UserProvider`とログイン画面で行っているため、個別のページでは不要
- 全ページがクライアント側取得（CSR）。投稿ごとのOGPは、ホスティング先が決まってからエッジ関数で差し込む予定

## 多言語対応（i18n）

画面に表示する固定の文言は、コードに直接書かず、翻訳ファイルに書く。

### 翻訳ファイル

- `src/lib/i18n/locales/{ja,en}/common.json` に、日本語と英語を同じキーで書く（ファイルは分けない）
- 画面ごとの文言は、エリア名のキーの下にまとめる（例：`setting.profile.title`、`manage.form.title`）。複数のエリアで使う文言はトップレベルに置く（例：`status.back`、`fetch.save`）
- キーは camelCase で書く
- キーの型は日本語の JSON から作られるため、存在しないキーは型エラーになる。英語の JSON にも同じキーを必ず追加する
- 文中に値を入れるときは `{{name}}` で補間する（文字列連結で組み立てない。語順が言語で変わるため）
- 英語の数による変化（単数・複数形）は `_one` / `_other` を使う

### 使い方

```tsx
const { t } = useTranslation()
<Main title={t('setting.profile.title')}>
```

- トースト文言は `Fetch` / `FetchError` をそのまま `handleToast` に渡す（`useToast` の中で翻訳する）
- API のエラーの `message` は i18n のキー（`error.*`）で返るので、翻訳せずにそのまま `handleToast` / `handleError` に渡す（`useToast` / `useApiError` が、i18n にあるキーなら翻訳し、無ければそのまま出す）
- BE がエラーの文言を増やしたときは、同じキーを `error` の下に ja / en とも追加する
- 日付の表示は `useDatetime` の `formatDatetime` / `formatDate` / `formatTimeAgo` を使う（表示中の言語で整形する）
- 金額の表示は `utils/functions/price.ts` の `formatPrice(amount, currency, i18n.language)` を使う（`Currency` の通貨と表示中の言語で整形する。`¥` などの通貨記号を直書きしない）
- 性別は ``t(`gender.${gender}`)``、都道府県の選択肢は `prefectures` の `key` から ``t(`prefecture.${key}`)`` で作る（保存する値は日本語のまま）
- ユーザーが入力した内容や API から返る値（投稿タイトル、カテゴリ名など）は翻訳しない

## コンポーネント設計

- 1ファイル1コンポーネント（default export）
- ロジックが複雑になったらカスタムフックに切り出す
- 1ページ = 1フォルダ（`components/pages/` の下）にし、URL と同じ階層に置く（`/media/video/$ulid` → `components/pages/media/video/detail/`）
- `index.tsx` はデータ取得（`useSuspenseQuery`）と `view.tsx` の呼び出しのみ。ルートが読み込む入口になる
- `view.tsx` にページの実装（表示・状態管理）を置く。データは props で受け取る
- そのページだけで使う scss・部品は、同じフォルダに置く。近いページで共有するもの（`Account.module.scss` など）は、共通の親フォルダに置く

```
components/pages/media/video/
  index.tsx        ← 一覧のデータ取得（/media/video）
  view.tsx         ← 一覧の表示
  detail/
    index.tsx      ← 詳細のデータ取得（/media/video/$ulid）
    view.tsx       ← 詳細の表示
```

## ディレクトリ構成の責務

| ディレクトリ | 責務 |
|------|------|
| `pages/` | 1ページ = 1フォルダ。`index.tsx` でデータ取得（`useSuspenseQuery`）、`view.tsx` でページの実装・状態管理 |
| `widgets/` | 複合コンポーネント（Modal, Card等） |
| `parts/` | 汎用UIコンポーネント（Button, Input等） |
| `hooks/` | カスタムフック |
| `api/` | APIクライアント関数 |
| `lib/routes.tsx` | URL とページの対応（TanStack Router のルート定義） |
| `lib/query/` | TanStack Queryの設定（`client.ts`）とクエリキー（`keys.ts`） |
| `types/` | 型定義 |
| `utils/` | ユーティリティ関数 |

## 依存方向

`parts/` ← `widgets/` ← `pages/` の片方向のみ依存する。逆方向や同階層への依存は禁止（ページ間で表示を共有するときだけ、`pages/` 同士の import を許容する。例: `recommend/index.tsx` が `home/view.tsx` を使う）。

`parts/` → `widgets/`・`pages/`、`widgets/` → `pages/` の import は、`eslint.config.mjs` の `import/no-restricted-paths` で検出する。

ただし、`widgets/` 内の同じフォルダ（同ファミリ）内の依存は許容する（例: `Status/RouteError` が `Status/Check`・`Status/Custom500` を使う）。

### parts は独立性を持つ

- `parts/` 配下のコンポーネントは他の `parts/` を import しない（最下層UIとしてそれ単体で動作する）
- レイアウト（縦並び・間隔等）は `VStack` / `HStack` などの parts に頼らず、自前の `<div>` + CSS（`display: flex` / `gap` 等）で実現する
- `widgets/` / `pages/` から parts を呼ぶ・複数 parts を組み合わせるのは正常な使い方

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
- `widgets/` / `pages/` ではグローバル CSS / 共有 mixin の利用を許容（ページ単位の構成のため）

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

コードを書いた後、必ず `pnpm check`（ESLint と `tsc --noEmit`）を実行する。

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
- 2026-10-07: 多言語対応（i18n）のルールを追加
- 2026-10-07: 言語の接頭辞（`/en`）を `{-$locale}` ルートからルーターの `rewrite` に移動
- 2026-10-07: `useAppRouter` を `useRouter` に名前を変更し、`window.location` / `window.history` の直接利用をなくす
- 2026-10-21: API のエラーの `message` を i18n のキー（`error.*`）として翻訳するようにした
- 2026-10-22: 金額の表示を `formatPrice` で通貨に合わせて整形するようにした
- 2026-10-22: ルートの`loader`で遷移前にデータを取る形を追加（ホーム・動画の詳細から）
- 2026-10-22: 全ページが`loader`に移ったため、`QueryCheck`の`fresh`を廃止
- 2026-10-22: `queryKeys`・`queryOptions`の名前を一覧は複数形、詳細は単数形、まとめたキーは`All`付きにそろえた
- 2026-11-02: 全ページを`useSuspenseQuery`に移し、取得中・エラーの表示をルートに任せた（`QueryCheck`を廃止）
