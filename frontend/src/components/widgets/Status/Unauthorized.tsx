import { useTranslation } from 'react-i18next'
import { useRouter } from 'components/hooks/useRouter'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import LoginRequired from 'components/widgets/Status/LoginRequired'

type LoginTitle = 'channel' | 'playlist' | 'follow' | 'follower' | 'series' | 'advertise' | 'manage' | 'profile' | 'mypage' | 'notification' | 'password' | 'payment' | 'withdrawal'

const loginTitles: { path: string; title: LoginTitle }[] = [
  { path: '/menu/channel', title: 'channel' },
  { path: '/menu/playlist', title: 'playlist' },
  { path: '/menu/follow', title: 'follow' },
  { path: '/menu/follower', title: 'follower' },
  { path: '/manage/series', title: 'series' },
  { path: '/manage/advertise', title: 'advertise' },
  { path: '/manage', title: 'manage' },
  { path: '/setting/profile', title: 'profile' },
  { path: '/setting/mypage', title: 'mypage' },
  { path: '/setting/notification', title: 'notification' },
  { path: '/setting/password', title: 'password' },
  { path: '/setting/payment', title: 'payment' },
  { path: '/account/withdrawal', title: 'withdrawal' },
]

export default function Unauthorized(): React.JSX.Element {
  const router = useRouter()
  const { t } = useTranslation()

  const loginTitle = loginTitles.find((l) => router.pathname === l.path || router.pathname.startsWith(`${l.path}/`))
  const content = loginTitle ? t('status.loginRequired', { title: t(`status.loginTitle.${loginTitle.title}`) }) : t('status.unauthorized')

  return (
    <Main title="Unauthorized">
      <LoginRequired content={content} />
      <Footer />
    </Main>
  )
}
