import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Currency } from 'utils/constants/enum'
import { priceAmount, priceText } from 'utils/functions/price'
import Input from 'components/parts/Input'
import ToggleCard from 'components/parts/Input/ToggleCard'
import SellerHint from 'components/widgets/SellerHint'
import TextEditor from 'components/widgets/TextEditor'

interface Props {
  isSale: boolean
  paidText: string
  price: number
  currency: Currency
  isAvailable: boolean
  isEnabled: boolean
  onSale: () => void
  onPaidText: (paidText: string) => void
  onPrice: (price: number) => void
}

export default function PaidTextInput(props: Props): React.JSX.Element {
  const { isSale, paidText, price, currency, isAvailable, isEnabled, onSale, onPaidText, onPrice } = props

  const { t } = useTranslation()
  const [text, setText] = useState<string>(priceText(price, currency))

  const isSellable = isAvailable && isEnabled

  const handlePrice = (e: ChangeEvent<HTMLInputElement>) => {
    setText(e.target.value)
    onPrice(priceAmount(e.target.value, currency))
  }

  const handlePaidText = (html: string) => onPaidText(html.trim() === '<p></p>' ? '' : html.trim())

  return (
    <>
      <ToggleCard label={t('manage.form.sale')} isActive={isSale} disable={!isSellable} onClick={isSellable ? onSale : undefined} />
      {!isSellable && <SellerHint isAvailable={isAvailable} />}
      {isSale && (
        <>
          <Input label={t('manage.form.price', { currency })} type="number" name="price" value={text} onChange={handlePrice} />
          <TextEditor label={t('manage.form.paidText')} value={paidText} onChange={handlePaidText} />
        </>
      )}
    </>
  )
}
