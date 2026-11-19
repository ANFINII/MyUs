import { useTranslation } from 'react-i18next'
import Main from 'components/layout/Main'
import SideTable from 'components/widgets/Table/Side'

const items = ['seller', 'representative', 'address', 'phone', 'email', 'price', 'extraFee', 'payment', 'paymentTiming', 'delivery', 'cancel', 'environment'] as const

export default function Commerce(): React.JSX.Element {
  const { t } = useTranslation()

  const rows = items.map((item) => ({ label: t(`menu.commerce.${item}.label`), content: t(`menu.commerce.${item}.content`) }))

  return (
    <Main title={t('menu.commerce.title')} type="table" isFooter={false}>
      <SideTable rows={rows} />
    </Main>
  )
}
