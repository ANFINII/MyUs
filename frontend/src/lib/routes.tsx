import { QueryClient } from '@tanstack/react-query'
import { AsyncRouteComponent, createRootRouteWithContext, createRoute, lazyRouteComponent, ResolveParams } from '@tanstack/react-router'
import {
  blogLoader,
  blogsLoader,
  chatLoader,
  chatsLoader,
  chatThreadLoader,
  comicLoader,
  comicsLoader,
  followersLoader,
  followsLoader,
  homeLoader,
  manageAdvertiseLoader,
  manageAdvertisesLoader,
  manageBlogLoader,
  manageBlogsLoader,
  manageChatLoader,
  manageChatsLoader,
  manageComicLoader,
  manageComicsLoader,
  manageCreateLoader,
  manageLoader,
  manageMusicLoader,
  manageMusicsLoader,
  managePictureLoader,
  managePicturesLoader,
  manageSeriesListLoader,
  manageSeriesLoader,
  manageVideoLoader,
  manageVideosLoader,
  musicLoader,
  musicsLoader,
  PageLoad,
  passwordResetLoader,
  pictureLoader,
  picturesLoader,
  playlistLoader,
  playlistsLoader,
  recommendLoader,
  settingMypageLoader,
  settingNotificationLoader,
  settingPasswordLoader,
  settingPaymentLoader,
  settingProfileLoader,
  signupLoader,
  subscribeChannelsLoader,
  userPageLoader,
  videoLoader,
  videosLoader,
} from 'lib/query/loaders'
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
  page('/media/video', () => import('components/pages/media/video'), videosLoader),
  page('/media/video/$ulid', () => import('components/pages/media/video/detail'), videoLoader),
  page('/media/music', () => import('components/pages/media/music'), musicsLoader),
  page('/media/music/$ulid', () => import('components/pages/media/music/detail'), musicLoader),
  page('/media/blog', () => import('components/pages/media/blog'), blogsLoader),
  page('/media/blog/$ulid', () => import('components/pages/media/blog/detail'), blogLoader),
  page('/media/comic', () => import('components/pages/media/comic'), comicsLoader),
  page('/media/comic/$ulid', () => import('components/pages/media/comic/detail'), comicLoader),
  page('/media/picture', () => import('components/pages/media/picture'), picturesLoader),
  page('/media/picture/$ulid', () => import('components/pages/media/picture/detail'), pictureLoader),
  page('/media/chat', () => import('components/pages/media/chat'), chatsLoader),
  page('/media/chat/$ulid', () => import('components/pages/media/chat/detail'), chatLoader),
  page('/media/chat/$ulid/thread/$messageUlid', () => import('components/pages/media/chat/detail'), chatThreadLoader),

  page('/menu/channel', () => import('components/pages/menu/channel'), subscribeChannelsLoader),
  page('/menu/playlist', () => import('components/pages/menu/playlist'), playlistsLoader),
  page('/menu/playlist/$ulid', () => import('components/pages/menu/playlist/detail'), playlistLoader),
  page('/menu/follow', () => import('components/pages/menu/follow'), followsLoader),
  page('/menu/follower', () => import('components/pages/menu/follower'), followersLoader),
  page('/menu/knowledge', () => import('components/pages/menu/knowledge')),
  page('/menu/userpolicy', () => import('components/pages/menu/userpolicy')),
  page('/menu/privacy', () => import('components/pages/menu/privacy')),
  page('/menu/commerce', () => import('components/pages/menu/commerce')),

  page('/account/login', () => import('components/pages/account/login')),
  page('/account/signup', () => import('components/pages/account/signup'), signupLoader),
  page('/account/signup/email', () => import('components/pages/account/signup/email')),
  page('/account/reset', () => import('components/pages/account/reset')),
  page('/account/reset/confirm', () => import('components/pages/account/reset/confirm'), passwordResetLoader),
  page('/account/reset/done', () => import('components/pages/account/reset/done')),
  page('/account/withdrawal', () => import('components/pages/account/withdrawal')),
  page('/account/withdrawal/confirm', () => import('components/pages/account/withdrawal/confirm')),

  page('/manage', () => import('components/pages/manage'), manageLoader),
  page('/manage/video', () => import('components/pages/manage/video'), manageVideosLoader),
  page('/manage/video/create', () => import('components/pages/manage/video/create'), manageCreateLoader),
  page('/manage/video/$ulid', () => import('components/pages/manage/video/edit'), manageVideoLoader),
  page('/manage/music', () => import('components/pages/manage/music'), manageMusicsLoader),
  page('/manage/music/create', () => import('components/pages/manage/music/create'), manageCreateLoader),
  page('/manage/music/$ulid', () => import('components/pages/manage/music/edit'), manageMusicLoader),
  page('/manage/blog', () => import('components/pages/manage/blog'), manageBlogsLoader),
  page('/manage/blog/create', () => import('components/pages/manage/blog/create'), manageCreateLoader),
  page('/manage/blog/$ulid', () => import('components/pages/manage/blog/edit'), manageBlogLoader),
  page('/manage/comic', () => import('components/pages/manage/comic'), manageComicsLoader),
  page('/manage/comic/create', () => import('components/pages/manage/comic/create'), manageCreateLoader),
  page('/manage/comic/$ulid', () => import('components/pages/manage/comic/edit'), manageComicLoader),
  page('/manage/picture', () => import('components/pages/manage/picture'), managePicturesLoader),
  page('/manage/picture/create', () => import('components/pages/manage/picture/create'), manageCreateLoader),
  page('/manage/picture/$ulid', () => import('components/pages/manage/picture/edit'), managePictureLoader),
  page('/manage/chat', () => import('components/pages/manage/chat'), manageChatsLoader),
  page('/manage/chat/create', () => import('components/pages/manage/chat/create'), manageCreateLoader),
  page('/manage/chat/$ulid', () => import('components/pages/manage/chat/edit'), manageChatLoader),
  page('/manage/series', () => import('components/pages/manage/series'), manageSeriesListLoader),
  page('/manage/series/$ulid', () => import('components/pages/manage/series/edit'), manageSeriesLoader),
  page('/manage/advertise', () => import('components/pages/manage/advertise'), manageAdvertisesLoader),
  page('/manage/advertise/create', () => import('components/pages/manage/advertise/create')),
  page('/manage/advertise/$ulid', () => import('components/pages/manage/advertise/edit'), manageAdvertiseLoader),

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
