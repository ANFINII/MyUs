import { useTranslation } from 'react-i18next'
import { loginPages } from 'utils/constants/login'
import { useRouter } from 'components/hooks/useRouter'
import Main from 'components/layout/Main'
import LoginRequired from 'components/widgets/Status/LoginRequired'

export default function Unauthorized(): React.JSX.Element {
  const router = useRouter()
  const { t } = useTranslation()

  const loginPage = loginPages.find((p) => router.pathname === p.path || router.pathname.startsWith(`${p.path}/`))
  const title = loginPage ? ('titleKey' in loginPage ? t(loginPage.titleKey) : loginPage.title) : t('status.login')

  return (
    <Main title={title} type="table">
      <LoginRequired />
    </Main>
  )
}
