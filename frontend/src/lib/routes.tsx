import { QueryClient } from '@tanstack/react-query'
import { AsyncRouteComponent, createRootRouteWithContext, createRoute, lazyRouteComponent, ResolveParams } from '@tanstack/react-router'
import { blogDetailLoader, blogListLoader, chatDetailLoader, chatListLoader, chatThreadLoader, comicDetailLoader, comicListLoader, followersLoader, followsLoader, homeLoader, manageAdvertiseEditLoader, manageAdvertiseListLoader, manageBlogEditLoader, manageBlogListLoader, manageChatEditLoader, manageChatListLoader, manageComicEditLoader, manageComicListLoader, manageCreateLoader, manageLoader, manageMusicEditLoader, manageMusicListLoader, managePictureEditLoader, managePictureListLoader, manageVideoEditLoader, manageVideoListLoader, musicDetailLoader, musicListLoader, PageLoad, pictureDetailLoader, pictureListLoader, recommendLoader, settingMypageLoader, settingNotificationLoader, settingPasswordLoader, settingPaymentLoader, settingProfileLoader, subscribeChannelsLoader, userPageLoader, videoDetailLoader, videoListLoader } from 'lib/query/loaders'
import PageLayout from 'components/layout/PageLayout'

type PageImport = () => Promise<{ default: () => React.JSX.Element }>
type PageLoader<TPath extends string> = (load: PageLoad<ResolveParams<TPath>>) => Promise<unknown>

export interface RouterContext {
  queryClient: QueryClient
}

const components = new Map<string, AsyncRouteComponent<unknown>>()
const rootRoute = createRootRouteWithContext<RouterContext>()({ component: PageLayout })

const lazyPage = (load: PageImport) => {
  const component = components.get(load.toString()) ?? lazyRouteComponent(load)
  components.set(load.toString(), component)
  return component
}

const page = <TPath extends string>(path: TPath, load: PageImport, loader?: PageLoader<TPath>) => {
  return createRoute({
    getParentRoute: () => rootRoute,
    path,
    component: lazyPage(load),
    loaderDeps: ({ search }) => search,
    loader: ({ context, params, deps }) => loader?.({ queryClient: context.queryClient, params: params as ResolveParams<TPath>, search: deps }),
  })
}

export const routeTree = rootRoute.addChildren([
  page('/', () => import('pages/index'), homeLoader),
  page('/recommend', () => import('pages/recommend'), recommendLoader),
  page('/userpage/$ulid', () => import('pages/userpage'), userPageLoader),
  page('/media/video', () => import('pages/media/video'), videoListLoader),
  page('/media/video/$ulid', () => import('pages/media/video/detail'), videoDetailLoader),
  page('/media/music', () => import('pages/media/music'), musicListLoader),
  page('/media/music/$ulid', () => import('pages/media/music/detail'), musicDetailLoader),
  page('/media/blog', () => import('pages/media/blog'), blogListLoader),
  page('/media/blog/$ulid', () => import('pages/media/blog/detail'), blogDetailLoader),
  page('/media/comic', () => import('pages/media/comic'), comicListLoader),
  page('/media/comic/$ulid', () => import('pages/media/comic/detail'), comicDetailLoader),
  page('/media/picture', () => import('pages/media/picture'), pictureListLoader),
  page('/media/picture/$ulid', () => import('pages/media/picture/detail'), pictureDetailLoader),
  page('/media/chat', () => import('pages/media/chat'), chatListLoader),
  page('/media/chat/$ulid', () => import('pages/media/chat/detail'), chatDetailLoader),
  page('/media/chat/$ulid/thread/$messageUlid', () => import('pages/media/chat/detail'), chatThreadLoader),

  page('/menu/channel', () => import('pages/menu/channel'), subscribeChannelsLoader),
  page('/menu/follow', () => import('pages/menu/follow'), followsLoader),
  page('/menu/follower', () => import('pages/menu/follower'), followersLoader),
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

  page('/manage', () => import('pages/manage'), manageLoader),
  page('/manage/video', () => import('pages/manage/video'), manageVideoListLoader),
  page('/manage/video/create', () => import('pages/manage/video/create'), manageCreateLoader),
  page('/manage/video/$ulid', () => import('pages/manage/video/edit'), manageVideoEditLoader),
  page('/manage/music', () => import('pages/manage/music'), manageMusicListLoader),
  page('/manage/music/create', () => import('pages/manage/music/create'), manageCreateLoader),
  page('/manage/music/$ulid', () => import('pages/manage/music/edit'), manageMusicEditLoader),
  page('/manage/blog', () => import('pages/manage/blog'), manageBlogListLoader),
  page('/manage/blog/create', () => import('pages/manage/blog/create'), manageCreateLoader),
  page('/manage/blog/$ulid', () => import('pages/manage/blog/edit'), manageBlogEditLoader),
  page('/manage/comic', () => import('pages/manage/comic'), manageComicListLoader),
  page('/manage/comic/create', () => import('pages/manage/comic/create'), manageCreateLoader),
  page('/manage/comic/$ulid', () => import('pages/manage/comic/edit'), manageComicEditLoader),
  page('/manage/picture', () => import('pages/manage/picture'), managePictureListLoader),
  page('/manage/picture/create', () => import('pages/manage/picture/create'), manageCreateLoader),
  page('/manage/picture/$ulid', () => import('pages/manage/picture/edit'), managePictureEditLoader),
  page('/manage/chat', () => import('pages/manage/chat'), manageChatListLoader),
  page('/manage/chat/create', () => import('pages/manage/chat/create'), manageCreateLoader),
  page('/manage/chat/$ulid', () => import('pages/manage/chat/edit'), manageChatEditLoader),
  page('/manage/advertise', () => import('pages/manage/advertise'), manageAdvertiseListLoader),
  page('/manage/advertise/create', () => import('pages/manage/advertise/create')),
  page('/manage/advertise/$ulid', () => import('pages/manage/advertise/edit'), manageAdvertiseEditLoader),

  page('/setting/profile', () => import('pages/setting/profile'), settingProfileLoader),
  page('/setting/profile/edit', () => import('pages/setting/profile/edit'), settingProfileLoader),
  page('/setting/mypage', () => import('pages/setting/mypage'), settingMypageLoader),
  page('/setting/mypage/edit', () => import('pages/setting/mypage/edit'), settingMypageLoader),
  page('/setting/mypage/channel/create', () => import('pages/setting/mypage/channel/create')),
  page('/setting/notification', () => import('pages/setting/notification'), settingNotificationLoader),
  page('/setting/password/change', () => import('pages/setting/password/change'), settingPasswordLoader),
  page('/setting/password/change-done', () => import('pages/setting/password/change-done'), settingPasswordLoader),
  page('/setting/payment', () => import('pages/setting/payment'), settingPaymentLoader),
  page('/setting/payment/change', () => import('pages/setting/payment/change'), settingPaymentLoader),
  page('/setting/payment/success', () => import('pages/setting/payment/success')),
  page('/setting/payment/cancel', () => import('pages/setting/payment/cancel')),
])
