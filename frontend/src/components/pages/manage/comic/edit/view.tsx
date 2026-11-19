import { useState, ChangeEvent } from 'react'
import { useTranslation } from 'react-i18next'
import { errorMessage } from 'lib/error'
import { Category } from 'types/internal/category'
import { Channel } from 'types/internal/channel'
import { ComicUpdateIn } from 'types/internal/media/input'
import { Comic } from 'types/internal/media/output'
import { PaymentSellerOut } from 'types/internal/payment'
import { putManageComic } from 'api/internal/manage/update'
import { Fetch, FetchError } from 'utils/constants/enum'
import { datetimeLocal, datetimeISO } from 'utils/functions/datetime'
import { previewUrl } from 'utils/functions/file'
import { paidPagesError } from 'utils/functions/price'
import { useLoading } from 'components/hooks/useLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import DatePicker from 'components/parts/Input/DatePicker'
import InputFile from 'components/parts/Input/File'
import SelectBox from 'components/parts/Input/SelectBox'
import Textarea from 'components/parts/Input/Textarea'
import ToggleCard from 'components/parts/Input/ToggleCard'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import ComicModal from 'components/widgets/Modal/Comic'
import PaidPagesInput from 'components/widgets/PaidPagesInput'
import style from '../../Form.module.scss'

interface Props {
  channels: Channel[]
  categories: Category[]
  seller: PaymentSellerOut
  data: Comic
}

export default function ManageComicEdit(props: Props): React.JSX.Element {
  const { channels, categories, seller, data } = props
  const { categoryUlid, title, content, freePages, publish, publishAt } = data
  const price = data.product?.price.amount ?? 0
  const currency = data.product?.price.currency ?? seller.currency

  const router = useRouter()
  const { t } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { error, validate } = useRequired()
  const { toast, handleToast } = useToast()
  const [isModal, setIsModal] = useState<boolean>(false)
  const [isSale, setIsSale] = useState<boolean>(data.product !== null)
  const [previewPages, setPreviewPages] = useState<string[]>([])
  const [values, setValues] = useState<ComicUpdateIn>({ categoryUlid, title, content, price, freePages, publish, publishAt: datetimeISO(publishAt) })

  const channelOptions = channels.map((c) => ({ label: c.name, value: c.ulid }))
  const categoryOptions = [{ label: t('manage.form.unselected'), value: '' }, ...categories.map((c) => ({ label: c.jpName, value: c.ulid }))]

  const handleBack = () => router.push('/manage/comic')
  const handleSelect = (e: ChangeEvent<HTMLSelectElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleFile = (file: File) => setValues({ ...values, image: file })
  const handleSale = () => setIsSale(!isSale)
  const handlePrice = (price: number) => setValues({ ...values, price })
  const handleFreePages = (freePages: number) => setValues({ ...values, freePages })
  const handlePublish = () => setValues({ ...values, publish: !values.publish })
  const handlePublishAt = (publishAt: string) => setValues({ ...values, publishAt: datetimeISO(publishAt) })

  const handleModal = () => {
    if (isModal) {
      previewPages.forEach((url) => URL.revokeObjectURL(url))
      setPreviewPages([])
    } else {
      setPreviewPages([values.image ? previewUrl(values.image) : data.image, ...data.pages])
    }
    setIsModal(!isModal)
  }

  const handleForm = async () => {
    const { categoryUlid, title, content } = values
    if (!validate({ categoryUlid, title, content })) return
    const paidError = isSale ? paidPagesError(values.price, values.freePages, data.pages.length) : ''
    if (paidError !== '') {
      handleToast(paidError, true)
      return
    }
    const request = isSale ? values : { ...values, price: 0, freePages: 0 }
    handleLoading(true)
    const ret = await putManageComic(data.ulid, request)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(errorMessage(ret.error, FetchError.Put), true)
      return
    }
    handleToast(Fetch.Save, false)
  }

  const button = (
    <HStack gap="4">
      <Button color="purple" size="s" name={t('manage.button.preview')} onClick={handleModal} />
      <Button color="green" size="s" name={t('manage.button.save')} loading={loading} onClick={handleForm} />
      <Button color="blue" size="s" name={t('status.back')} onClick={handleBack} />
    </HStack>
  )

  return (
    <Main title="Comic" type="table" toast={toast} isFooter={false} button={button}>
      <form className={style.form} method="POST" action="" encType="multipart/form-data">
        <VStack gap="8">
          <ToggleCard label={t('manage.form.publish')} isActive={values.publish} onClick={handlePublish} />
          <DatePicker label={t('manage.form.publishAt')} name="publishAt" value={datetimeLocal(values.publishAt)} onChange={handlePublishAt} isTime />
          <SelectBox label={t('manage.form.channel')} name="channelUlid" value={data.channel.ulid} options={channelOptions} disabled />
          <SelectBox label={t('manage.form.category')} name="categoryUlid" value={values.categoryUlid} options={categoryOptions} required error={error} onChange={handleSelect} />
          <Input label={t('manage.form.title')} name="title" maxLength={100} value={values.title} required error={error} onChange={handleInput} />
          <Textarea label={t('manage.form.content')} name="content" value={values.content} required error={error} onChange={handleText} />
          <InputFile label={t('manage.form.thumbnail')} accept="image/*" required error={error} onChange={handleFile} />
          <PaidPagesInput
            isSale={isSale}
            price={values.price}
            freePages={values.freePages}
            currency={currency}
            isAvailable={seller.isAvailable || data.product !== null}
            isEnabled={seller.isEnabled || data.product !== null}
            onSale={handleSale}
            onPrice={handlePrice}
            onFreePages={handleFreePages}
          />
        </VStack>
      </form>
      <ComicModal open={isModal} onClose={handleModal} pages={previewPages} />
    </Main>
  )
}
