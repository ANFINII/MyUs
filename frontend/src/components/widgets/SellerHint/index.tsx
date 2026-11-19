import { useTranslation } from 'react-i18next'
import IconInfo from 'components/parts/Icon/Info'
import Link from 'components/parts/Link'
import style from './SellerHint.module.scss'

interface Props {
  isAvailable: boolean
}

export default function SellerHint(props: Props): React.JSX.Element {
  const { isAvailable } = props

  const { t } = useTranslation()

  return (
    <div className={style.hint}>
      <IconInfo size="14" className={style.hint_icon} />
      <span>{isAvailable ? t('manage.form.saleSellerHint') : t('manage.form.salePlanHint')}</span>
      <Link href="/setting/payment" className={style.hint_link}>
        {t('manage.form.saleSetting')}
      </Link>
    </div>
  )
}
