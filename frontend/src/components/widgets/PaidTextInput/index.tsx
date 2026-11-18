import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Currency } from 'utils/constants/enum'
import { priceAmount, priceText } from 'utils/functions/price'
import IconInfo from 'components/parts/Icon/Info'
import Input from 'components/parts/Input'
import Link from 'components/parts/Link'
import TextEditor from 'components/widgets/TextEditor'
import style from './PaidTextInput.module.scss'

interface Props {
  paidText: string
  price: number
  currency: Currency
  isAvailable: boolean
  isEnabled: boolean
  onPaidText: (paidText: string) => void
  onPrice: (price: number) => void
}

export default function PaidTextInput(props: Props): React.JSX.Element {
  const { paidText, price, currency, isAvailable, isEnabled, onPaidText, onPrice } = props

  const { t } = useTranslation()
  const [text, setText] = useState<string>(priceText(price, currency))

  const handlePrice = (e: ChangeEvent<HTMLInputElement>) => {
    setText(e.target.value)
    onPrice(priceAmount(e.target.value, currency))
  }

  const handlePaidText = (html: string) => onPaidText(html.trim() === '<p></p>' ? '' : html.trim())

  if (!isAvailable || !isEnabled) {
    return (
      <div className={style.hint}>
        <IconInfo size="14" className={style.hint_icon} />
        <span>{isAvailable ? t('manage.form.paidSellerHint') : t('manage.form.paidPlanHint')}</span>
        <Link href="/setting/payment" className={style.hint_link}>
          {t('manage.form.paidSetting')}
        </Link>
      </div>
    )
  }

  return (
    <>
      <Input label={t('manage.form.price', { currency })} type="number" name="price" value={text} onChange={handlePrice} />
      <TextEditor label={t('manage.form.paidText')} value={paidText} onChange={handlePaidText} />
    </>
  )
}
