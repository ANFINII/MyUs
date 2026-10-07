import { useTranslation } from 'react-i18next'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import BackLogin from 'components/widgets/Status/Login'

export default function Unauthorized(): React.JSX.Element {
  const { t } = useTranslation()

  return (
    <Main title="Unauthorized">
      <BackLogin content={t('status.unauthorized')} />
      <Footer />
    </Main>
  )
}
