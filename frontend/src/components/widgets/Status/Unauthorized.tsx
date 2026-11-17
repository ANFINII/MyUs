import { useTranslation } from 'react-i18next'
import { useRouter } from 'components/hooks/useRouter'
import Main from 'components/layout/Main'
import LoginRequired from 'components/widgets/Status/LoginRequired'

export default function Unauthorized(): React.JSX.Element {
  const router = useRouter()
  const { t } = useTranslation()

  const loginPages = [
    { path: '/menu/channel', title: 'Channel', name: t('status.loginTitle.channel') },
    { path: '/menu/playlist', title: 'Playlist', name: t('status.loginTitle.playlist') },
    { path: '/menu/follow', title: 'Follow', name: t('status.loginTitle.follow') },
    { path: '/menu/follower', title: 'Follower', name: t('status.loginTitle.follower') },
    { path: '/manage/video', title: 'Video', name: t('status.loginTitle.manage') },
    { path: '/manage/music', title: 'Music', name: t('status.loginTitle.manage') },
    { path: '/manage/blog', title: 'Blog', name: t('status.loginTitle.manage') },
    { path: '/manage/comic', title: 'Comic', name: t('status.loginTitle.manage') },
    { path: '/manage/picture', title: 'Picture', name: t('status.loginTitle.manage') },
    { path: '/manage/chat', title: 'Chat', name: t('status.loginTitle.manage') },
    { path: '/manage/series', title: 'Series', name: t('status.loginTitle.series') },
    { path: '/manage/advertise', title: 'Advertise', name: t('status.loginTitle.advertise') },
    { path: '/manage', title: t('manage.title'), name: t('status.loginTitle.manage') },
    { path: '/setting/profile', title: t('setting.profile.title'), name: t('status.loginTitle.profile') },
    { path: '/setting/mypage', title: t('setting.mypage.title'), name: t('status.loginTitle.mypage') },
    { path: '/setting/notification', title: t('setting.notification.title'), name: t('status.loginTitle.notification') },
    { path: '/setting/password', title: t('setting.password.title'), name: t('status.loginTitle.password') },
    { path: '/setting/payment', title: t('setting.payment.title'), name: t('status.loginTitle.payment') },
    { path: '/account/withdrawal', title: t('account.withdrawal.title'), name: t('status.loginTitle.withdrawal') },
  ]
  const loginPage = loginPages.find((p) => router.pathname === p.path || router.pathname.startsWith(`${p.path}/`))
  const title = loginPage ? loginPage.title : t('status.login')
  const content = loginPage ? t('status.loginRequired', { title: loginPage.name }) : t('status.unauthorized')

  return (
    <Main title={title} type="table">
      <LoginRequired content={content} />
    </Main>
  )
}
