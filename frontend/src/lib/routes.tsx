import { QueryClient } from '@tanstack/react-query'
import { AnyRoute, createRootRouteWithContext, createRoute, lazyRouteComponent, Outlet, ResolveParams } from '@tanstack/react-router'
import { homeLoader, PageLoad, videoDetailLoader } from 'lib/query/loaders'
import { useRouter } from 'components/hooks/useRouter'
import Layout from 'components/layout'
import { ErrorBoundary } from 'components/parts/ErrorBoundary'
import Unexpected from 'components/widgets/Status/Unexpected'

type PageImport = () => Promise<{ default: () => React.JSX.Element }>

type PageLoader<TPath extends string> = (load: PageLoad<ResolveParams<TPath>>) => Promise<unknown>

export interface RouterContext {
  queryClient: QueryClient
}

function RootLayout(): React.JSX.Element {
  const router = useRouter()

  return (
    <Layout>
      <ErrorBoundary fallback={<Unexpected />} resetKeys={[router.pathname]}>
        <Outlet />
      </ErrorBoundary>
    </Layout>
  )
}

const rootRoute = createRootRouteWithContext<RouterContext>()({ component: RootLayout })

const page = <TPath extends string>(path: TPath, load: PageImport, loader?: PageLoader<TPath>) => {
  return createRoute({
    getParentRoute: () => rootRoute,
    path,
    component: lazyRouteComponent(load),
    loaderDeps: ({ search }) => search,
    loader: ({ context, params, deps }) => loader?.({ queryClient: context.queryClient, params: params as ResolveParams<TPath>, search: deps }),
  })
}

const nest = <TParent extends AnyRoute>(parent: TParent, paths: string[]) => {
  return parent.addChildren(paths.map((path) => createRoute({ getParentRoute: () => parent, path, component: () => null })))
}

export const routeTree = rootRoute.addChildren([
  page('/', () => import('pages/index'), homeLoader),
  page('/recommend', () => import('pages/recommend')),
  page('/media/video', () => import('pages/media/video')),
  page('/media/video/$ulid', () => import('pages/media/video/detail'), videoDetailLoader),
  page('/media/music', () => import('pages/media/music')),
  page('/media/music/$ulid', () => import('pages/media/music/detail')),
  page('/media/blog', () => import('pages/media/blog')),
  page('/media/blog/$ulid', () => import('pages/media/blog/detail')),
  page('/media/comic', () => import('pages/media/comic')),
  page('/media/comic/$ulid', () => import('pages/media/comic/detail')),
  page('/media/picture', () => import('pages/media/picture')),
  page('/media/picture/$ulid', () => import('pages/media/picture/detail')),
  page('/media/chat', () => import('pages/media/chat')),
  nest(page('/media/chat/$ulid', () => import('pages/media/chat/detail')), ['/', '/thread/$messageUlid']),
  page('/userpage/$ulid', () => import('pages/userpage')),

  page('/menu/channel', () => import('pages/menu/channel')),
  page('/menu/follow', () => import('pages/menu/follow')),
  page('/menu/follower', () => import('pages/menu/follower')),
  page('/menu/knowledge', () => import('pages/menu/knowledge')),
  page('/menu/userpolicy', () => import('pages/menu/userpolicy')),

  page('/account/login', () => import('pages/account/login')),
  page('/account/signup', () => import('pages/account/signup')),
  page('/account/signup/email', () => import('pages/account/signup/email')),
  page('/account/reset', () => import('pages/account/reset')),
  page('/account/reset/confirm', () => import('pages/account/reset/confirm')),
  page('/account/reset/done', () => import('pages/account/reset/done')),
  page('/account/withdrawal', () => import('pages/account/withdrawal')),
  page('/account/withdrawal/confirm', () => import('pages/account/withdrawal/confirm')),

  page('/manage', () => import('pages/manage')),
  page('/manage/video', () => import('pages/manage/video')),
  page('/manage/video/create', () => import('pages/manage/video/create')),
  page('/manage/video/$ulid', () => import('pages/manage/video/edit')),
  page('/manage/music', () => import('pages/manage/music')),
  page('/manage/music/create', () => import('pages/manage/music/create')),
  page('/manage/music/$ulid', () => import('pages/manage/music/edit')),
  page('/manage/blog', () => import('pages/manage/blog')),
  page('/manage/blog/create', () => import('pages/manage/blog/create')),
  page('/manage/blog/$ulid', () => import('pages/manage/blog/edit')),
  page('/manage/comic', () => import('pages/manage/comic')),
  page('/manage/comic/create', () => import('pages/manage/comic/create')),
  page('/manage/comic/$ulid', () => import('pages/manage/comic/edit')),
  page('/manage/picture', () => import('pages/manage/picture')),
  page('/manage/picture/create', () => import('pages/manage/picture/create')),
  page('/manage/picture/$ulid', () => import('pages/manage/picture/edit')),
  page('/manage/chat', () => import('pages/manage/chat')),
  page('/manage/chat/create', () => import('pages/manage/chat/create')),
  page('/manage/chat/$ulid', () => import('pages/manage/chat/edit')),
  page('/manage/advertise', () => import('pages/manage/advertise')),
  page('/manage/advertise/create', () => import('pages/manage/advertise/create')),
  page('/manage/advertise/$ulid', () => import('pages/manage/advertise/edit')),

  page('/setting/profile', () => import('pages/setting/profile')),
  page('/setting/profile/edit', () => import('pages/setting/profile/edit')),
  page('/setting/mypage', () => import('pages/setting/mypage')),
  page('/setting/mypage/edit', () => import('pages/setting/mypage/edit')),
  page('/setting/mypage/channel/create', () => import('pages/setting/mypage/channel/create')),
  page('/setting/notification', () => import('pages/setting/notification')),
  page('/setting/password/change', () => import('pages/setting/password/change')),
  page('/setting/password/change-done', () => import('pages/setting/password/change-done')),
  page('/setting/payment', () => import('pages/setting/payment')),
  page('/setting/payment/change', () => import('pages/setting/payment/change')),
  page('/setting/payment/success', () => import('pages/setting/payment/success')),
  page('/setting/payment/cancel', () => import('pages/setting/payment/cancel')),
])
