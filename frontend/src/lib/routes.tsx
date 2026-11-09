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
  page('/', () => import('components/pages/home'), homeLoader),
  page('/recommend', () => import('components/pages/recommend'), recommendLoader),
  page('/userpage/$ulid', () => import('components/pages/userpage'), userPageLoader),
  page('/media/video', () => import('components/pages/media/video'), videoListLoader),
  page('/media/video/$ulid', () => import('components/pages/media/video/detail'), videoDetailLoader),
  page('/media/music', () => import('components/pages/media/music'), musicListLoader),
  page('/media/music/$ulid', () => import('components/pages/media/music/detail'), musicDetailLoader),
  page('/media/blog', () => import('components/pages/media/blog'), blogListLoader),
  page('/media/blog/$ulid', () => import('components/pages/media/blog/detail'), blogDetailLoader),
  page('/media/comic', () => import('components/pages/media/comic'), comicListLoader),
  page('/media/comic/$ulid', () => import('components/pages/media/comic/detail'), comicDetailLoader),
  page('/media/picture', () => import('components/pages/media/picture'), pictureListLoader),
  page('/media/picture/$ulid', () => import('components/pages/media/picture/detail'), pictureDetailLoader),
  page('/media/chat', () => import('components/pages/media/chat'), chatListLoader),
  page('/media/chat/$ulid', () => import('components/pages/media/chat/detail'), chatDetailLoader),
  page('/media/chat/$ulid/thread/$messageUlid', () => import('components/pages/media/chat/detail'), chatThreadLoader),

  page('/menu/channel', () => import('components/pages/menu/channel'), subscribeChannelsLoader),
  page('/menu/follow', () => import('components/pages/menu/follow'), followsLoader),
  page('/menu/follower', () => import('components/pages/menu/follower'), followersLoader),
  page('/menu/knowledge', () => import('components/pages/menu/knowledge')),
  page('/menu/userpolicy', () => import('components/pages/menu/userpolicy')),
  page('/menu/privacy', () => import('components/pages/menu/privacy')),
  page('/menu/commerce', () => import('components/pages/menu/commerce')),

  page('/account/login', () => import('components/pages/account/login')),
  page('/account/signup', () => import('components/pages/account/signup')),
  page('/account/signup/email', () => import('components/pages/account/signup/email')),
  page('/account/reset', () => import('components/pages/account/reset')),
  page('/account/reset/confirm', () => import('components/pages/account/reset/confirm')),
  page('/account/reset/done', () => import('components/pages/account/reset/done')),
  page('/account/withdrawal', () => import('components/pages/account/withdrawal')),
  page('/account/withdrawal/confirm', () => import('components/pages/account/withdrawal/confirm')),

  page('/manage', () => import('components/pages/manage'), manageLoader),
  page('/manage/video', () => import('components/pages/manage/video'), manageVideoListLoader),
  page('/manage/video/create', () => import('components/pages/manage/video/create'), manageCreateLoader),
  page('/manage/video/$ulid', () => import('components/pages/manage/video/edit'), manageVideoEditLoader),
  page('/manage/music', () => import('components/pages/manage/music'), manageMusicListLoader),
  page('/manage/music/create', () => import('components/pages/manage/music/create'), manageCreateLoader),
  page('/manage/music/$ulid', () => import('components/pages/manage/music/edit'), manageMusicEditLoader),
  page('/manage/blog', () => import('components/pages/manage/blog'), manageBlogListLoader),
  page('/manage/blog/create', () => import('components/pages/manage/blog/create'), manageCreateLoader),
  page('/manage/blog/$ulid', () => import('components/pages/manage/blog/edit'), manageBlogEditLoader),
  page('/manage/comic', () => import('components/pages/manage/comic'), manageComicListLoader),
  page('/manage/comic/create', () => import('components/pages/manage/comic/create'), manageCreateLoader),
  page('/manage/comic/$ulid', () => import('components/pages/manage/comic/edit'), manageComicEditLoader),
  page('/manage/picture', () => import('components/pages/manage/picture'), managePictureListLoader),
  page('/manage/picture/create', () => import('components/pages/manage/picture/create'), manageCreateLoader),
  page('/manage/picture/$ulid', () => import('components/pages/manage/picture/edit'), managePictureEditLoader),
  page('/manage/chat', () => import('components/pages/manage/chat'), manageChatListLoader),
  page('/manage/chat/create', () => import('components/pages/manage/chat/create'), manageCreateLoader),
  page('/manage/chat/$ulid', () => import('components/pages/manage/chat/edit'), manageChatEditLoader),
  page('/manage/advertise', () => import('components/pages/manage/advertise'), manageAdvertiseListLoader),
  page('/manage/advertise/create', () => import('components/pages/manage/advertise/create')),
  page('/manage/advertise/$ulid', () => import('components/pages/manage/advertise/edit'), manageAdvertiseEditLoader),

  page('/setting/profile', () => import('components/pages/setting/profile'), settingProfileLoader),
  page('/setting/profile/edit', () => import('components/pages/setting/profile/edit'), settingProfileLoader),
  page('/setting/mypage', () => import('components/pages/setting/mypage'), settingMypageLoader),
  page('/setting/mypage/edit', () => import('components/pages/setting/mypage/edit'), settingMypageLoader),
  page('/setting/mypage/channel/create', () => import('components/pages/setting/mypage/channel/create')),
  page('/setting/notification', () => import('components/pages/setting/notification'), settingNotificationLoader),
  page('/setting/password/change', () => import('components/pages/setting/password/change'), settingPasswordLoader),
  page('/setting/password/change-done', () => import('components/pages/setting/password/change-done'), settingPasswordLoader),
  page('/setting/payment', () => import('components/pages/setting/payment'), settingPaymentLoader),
  page('/setting/payment/change', () => import('components/pages/setting/payment/change'), settingPaymentLoader),
  page('/setting/payment/success', () => import('components/pages/setting/payment/success')),
  page('/setting/payment/cancel', () => import('components/pages/setting/payment/cancel')),
])
