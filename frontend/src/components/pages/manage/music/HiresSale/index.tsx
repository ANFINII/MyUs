import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQueryClient } from '@tanstack/react-query'
import { errorMessage } from 'lib/error'
import { queryKeys } from 'lib/query/keys'
import { MusicHiresIn } from 'types/internal/media/input'
import { MusicHires } from 'types/internal/media/output'
import { PaymentSellerOut, Product } from 'types/internal/payment'
import { deleteManageMusicHires } from 'api/internal/manage/delete'
import { putManageMusicHires } from 'api/internal/manage/update'
import { Fetch, FetchError } from 'utils/constants/enum'
import { flacHires, hiresError, hiresLabel } from 'utils/functions/hires'
import { priceAmount, priceText } from 'utils/functions/price'
import { useLoading } from 'components/hooks/useLoading'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import InputFile from 'components/parts/Input/File'
import ToggleCard from 'components/parts/Input/ToggleCard'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import SellerHint from 'components/widgets/SellerHint'
import style from './HiresSale.module.scss'

interface Props {
  ulid: string
  seller: PaymentSellerOut
  hires: MusicHires | null
  product: Product | null
  handleToast: (content: string, isError: boolean) => void
}

export default function HiresSale(props: Props): React.JSX.Element {
  const { ulid, seller, hires, product, handleToast } = props

  const { t } = useTranslation()
  const queryClient = useQueryClient()
  const { loading, handleLoading } = useLoading()
  const currency = product?.price.currency ?? seller.currency
  const [file, setFile] = useState<File | null>(null)
  const [fileHires, setFileHires] = useState<MusicHires | null>(null)
  const [text, setText] = useState<string>(priceText(product?.price.amount ?? 0, currency))
  const [isSale, setIsSale] = useState<boolean>(hires !== null)

  const isAvailable = seller.isAvailable || hires !== null
  const isEnabled = seller.isEnabled || hires !== null
  const isSellable = isAvailable && isEnabled
  const selectedHires = file === null ? hires : fileHires

  const handleSale = () => setIsSale(!isSale)
  const handlePrice = (e: ChangeEvent<HTMLInputElement>) => setText(e.target.value)

  const handleFile = async (selected: File) => {
    setFile(selected)
    setFileHires(await flacHires(selected))
  }

  const handleSave = async () => {
    const price = priceAmount(text, currency)
    const error = hiresError(selectedHires, price)
    if (error) {
      handleToast(error, true)
      return
    }
    const request: MusicHiresIn = file === null ? { price } : { price, hires: file }
    handleLoading(true)
    const ret = await putManageMusicHires(ulid, request)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(errorMessage(ret.error, FetchError.Put), true)
      return
    }
    setFile(null)
    await queryClient.invalidateQueries({ queryKey: queryKeys.manageMusic(ulid) })
    handleToast(Fetch.Save, false)
  }

  const handleStop = async () => {
    handleLoading(true)
    const ret = await deleteManageMusicHires(ulid)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(errorMessage(ret.error, FetchError.Delete), true)
      return
    }
    setFile(null)
    setText('')
    setIsSale(false)
    await queryClient.invalidateQueries({ queryKey: queryKeys.manageMusic(ulid) })
    handleToast(Fetch.Delete, false)
  }

  return (
    <>
      <ToggleCard label={t('manage.form.sale')} isActive={isSale} disable={!isSellable || hires !== null} onClick={isSellable && hires === null ? handleSale : undefined} />
      {!isSellable && <SellerHint isAvailable={isAvailable} />}
      {isSale && (
        <VStack gap="4" className={style.hires}>
          <p className={style.hires_title}>{t('manage.hires.title')}</p>
          <InputFile label={t('manage.hires.file')} accept=".flac,audio/flac" onChange={handleFile} />
          <p className={style.hires_note}>{selectedHires === null ? t('manage.hires.fileHint') : hiresLabel(selectedHires)}</p>
          <Input label={t('manage.form.price', { currency })} type="number" name="hiresPrice" value={text} onChange={handlePrice} />
          <HStack gap="4">
            <Button color="green" size="s" name={t('manage.button.save')} loading={loading} onClick={handleSave} />
            {hires !== null && <Button color="red" size="s" name={t('manage.hires.stop')} loading={loading} onClick={handleStop} />}
          </HStack>
        </VStack>
      )}
    </>
  )
}
