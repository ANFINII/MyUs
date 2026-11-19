import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Currency } from 'utils/constants/enum'
import { priceAmount, priceText } from 'utils/functions/price'
import Input from 'components/parts/Input'
import ToggleCard from 'components/parts/Input/ToggleCard'
import SellerHint from 'components/widgets/SellerHint'

interface Props {
  isSale: boolean
  price: number
  freePages: number
  currency: Currency
  isAvailable: boolean
  isEnabled: boolean
  onSale: () => void
  onPrice: (price: number) => void
  onFreePages: (freePages: number) => void
}

export default function PaidPagesInput(props: Props): React.JSX.Element {
  const { isSale, price, freePages, currency, isAvailable, isEnabled, onSale, onPrice, onFreePages } = props

  const { t } = useTranslation()
  const [text, setText] = useState<string>(priceText(price, currency))

  const isSellable = isAvailable && isEnabled

  const handlePrice = (e: ChangeEvent<HTMLInputElement>) => {
    setText(e.target.value)
    onPrice(priceAmount(e.target.value, currency))
  }

  const handleFreePages = (e: ChangeEvent<HTMLInputElement>) => onFreePages(Number(e.target.value))

  return (
    <>
      <ToggleCard label={t('manage.form.sale')} isActive={isSale} disable={!isSellable} onClick={isSellable ? onSale : undefined} />
      {!isSellable && <SellerHint isAvailable={isAvailable} />}
      {isSale && (
        <>
          <Input label={t('manage.form.price', { currency })} type="number" name="price" value={text} onChange={handlePrice} />
          <Input label={t('manage.form.freePages')} type="number" name="freePages" value={String(freePages)} onChange={handleFreePages} />
        </>
      )}
    </>
  )
}
