import { useTranslation } from 'react-i18next'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import LoginRequired from 'components/widgets/Status/LoginRequired'

export default function Unauthorized(): React.JSX.Element {
  const { t } = useTranslation()

  return (
    <Main title="Unauthorized">
      <LoginRequired content={t('status.unauthorized')} />
      <Footer />
    </Main>
  )
}
