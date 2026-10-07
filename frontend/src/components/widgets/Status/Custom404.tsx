import { useTranslation } from 'react-i18next'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import BackError from 'components/widgets/Status/Back'

export default function Custom404(): React.JSX.Element {
  const { t } = useTranslation()

  return (
    <Main title="404 Not Found">
      <BackError content={t('status.notFound')} />
      <Footer />
    </Main>
  )
}
