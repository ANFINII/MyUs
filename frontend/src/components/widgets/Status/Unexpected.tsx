import { useTranslation } from 'react-i18next'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import BackError from 'components/widgets/Status/Back'

export default function Unexpected(): React.JSX.Element {
  const { t } = useTranslation()

  return (
    <Main title="Unexpected Error">
      <BackError content={t('status.unexpected')} />
      <Footer />
    </Main>
  )
}
