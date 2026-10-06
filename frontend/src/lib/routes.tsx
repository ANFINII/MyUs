import { createRootRoute, createRoute, lazyRouteComponent, notFound, Outlet } from '@tanstack/react-router'
import { LOCALES } from 'lib/i18n'
import { useAppRouter } from 'components/hooks/useAppRouter'
import Layout from 'components/layout'
import { ErrorBoundary } from 'components/parts/ErrorBoundary'
import Unexpected from 'components/widgets/Status/Unexpected'

type PageImport = () => Promise<{ default: () => React.JSX.Element }>

function RootLayout(): React.JSX.Element {
  const router = useAppRouter()

  return (
    <Layout>
      <ErrorBoundary fallback={<Unexpected />} resetKeys={[router.pathname]}>
        <Outlet />
      </ErrorBoundary>
    </Layout>
  )
}

const rootRoute = createRootRoute({ component: RootLayout })

const localeRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '{-$locale}',
  beforeLoad: ({ params }) => {
    if (params.locale !== undefined && !LOCALES.includes(params.locale)) throw notFound()
  },
})

const page = <TPath extends string>(path: TPath, load: PageImport) => {
  return createRoute({ getParentRoute: () => localeRoute, path, component: lazyRouteComponent(load) })
}

const chatRoute = page('/media/chat/$ulid', () => import('pages/media/chat/[ulid]'))
const chatIndexRoute = createRoute({ getParentRoute: () => chatRoute, path: '/', component: () => null })
const chatThreadRoute = createRoute({ getParentRoute: () => chatRoute, path: '/thread/$messageUlid', component: () => null })

export const routeTree = rootRoute.addChildren([
  localeRoute.addChildren([
    page('/', () => import('pages/index')),
    page('/recommend', () => import('pages/recommend')),
    page('/media/video', () => import('pages/media/video')),
    page('/media/video/$ulid', () => import('pages/media/video/[ulid]')),
    page('/media/music', () => import('pages/media/music')),
    page('/media/music/$ulid', () => import('pages/media/music/[ulid]')),
    page('/media/blog', () => import('pages/media/blog')),
    page('/media/blog/$ulid', () => import('pages/media/blog/[ulid]')),
    page('/media/comic', () => import('pages/media/comic')),
    page('/media/comic/$ulid', () => import('pages/media/comic/[ulid]')),
    page('/media/picture', () => import('pages/media/picture')),
    page('/media/picture/$ulid', () => import('pages/media/picture/[ulid]')),
    page('/media/chat', () => import('pages/media/chat')),
    chatRoute.addChildren([chatIndexRoute, chatThreadRoute]),
    page('/userpage/$ulid', () => import('pages/userpage/[ulid]')),

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
    page('/manage/video/$ulid', () => import('pages/manage/video/[ulid]')),
    page('/manage/music', () => import('pages/manage/music')),
    page('/manage/music/create', () => import('pages/manage/music/create')),
    page('/manage/music/$ulid', () => import('pages/manage/music/[ulid]')),
    page('/manage/blog', () => import('pages/manage/blog')),
    page('/manage/blog/create', () => import('pages/manage/blog/create')),
    page('/manage/blog/$ulid', () => import('pages/manage/blog/[ulid]')),
    page('/manage/comic', () => import('pages/manage/comic')),
    page('/manage/comic/create', () => import('pages/manage/comic/create')),
    page('/manage/comic/$ulid', () => import('pages/manage/comic/[ulid]')),
    page('/manage/picture', () => import('pages/manage/picture')),
    page('/manage/picture/create', () => import('pages/manage/picture/create')),
    page('/manage/picture/$ulid', () => import('pages/manage/picture/[ulid]')),
    page('/manage/chat', () => import('pages/manage/chat')),
    page('/manage/chat/create', () => import('pages/manage/chat/create')),
    page('/manage/chat/$ulid', () => import('pages/manage/chat/[ulid]')),
    page('/manage/advertise', () => import('pages/manage/advertise')),
    page('/manage/advertise/create', () => import('pages/manage/advertise/create')),
    page('/manage/advertise/$ulid', () => import('pages/manage/advertise/[ulid]')),

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
  ]),
])
