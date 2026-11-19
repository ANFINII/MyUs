import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Currency } from 'utils/constants/enum'
import { priceAmount, priceText } from 'utils/functions/price'
import Input from 'components/parts/Input'
import SellerHint from 'components/widgets/SellerHint'

interface Props {
  price: number
  freePages: number
  currency: Currency
  isAvailable: boolean
  isEnabled: boolean
  onPrice: (price: number) => void
  onFreePages: (freePages: number) => void
}

export default function PaidPagesInput(props: Props): React.JSX.Element {
  const { price, freePages, currency, isAvailable, isEnabled, onPrice, onFreePages } = props

  const { t } = useTranslation()
  const [text, setText] = useState<string>(priceText(price, currency))

  const handlePrice = (e: ChangeEvent<HTMLInputElement>) => {
    setText(e.target.value)
    onPrice(priceAmount(e.target.value, currency))
  }

  const handleFreePages = (e: ChangeEvent<HTMLInputElement>) => onFreePages(Number(e.target.value))

  if (!isAvailable || !isEnabled) return <SellerHint isAvailable={isAvailable} />

  return (
    <>
      <Input label={t('manage.form.price', { currency })} type="number" name="price" value={text} onChange={handlePrice} />
      <Input label={t('manage.form.freePages')} type="number" name="freePages" value={String(freePages)} onChange={handleFreePages} />
    </>
  )
}
