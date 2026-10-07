import { useTranslation } from 'react-i18next'
import style from './CurrentBanner.module.scss'

interface Props {
  planName: string
}

export default function CurrentBanner(props: Props): React.JSX.Element {
  const { planName } = props

  const { t } = useTranslation()

  return (
    <div className={style.current}>
      <span className={style.label}>{t('setting.payment.currentPlan')}</span>
      <span className={style.plan}>{planName}</span>
    </div>
  )
}
