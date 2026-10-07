import { useTranslation } from 'react-i18next'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import BackError from 'components/widgets/Status/Back'

export default function Custom500(): React.JSX.Element {
  const { t } = useTranslation()

  return (
    <Main title="500 Server Error">
      <BackError content={t('status.serverError')} />
      <Footer />
    </Main>
  )
}
