import { useState, ChangeEvent } from 'react'
import { useTranslation } from 'react-i18next'
import { errorMessage } from 'lib/error'
import { Category } from 'types/internal/category'
import { Channel } from 'types/internal/channel'
import { BlogUpdateIn } from 'types/internal/media/input'
import { Blog } from 'types/internal/media/output'
import { PaymentSellerOut } from 'types/internal/payment'
import { putManageBlog } from 'api/internal/manage/update'
import { Fetch, FetchError } from 'utils/constants/enum'
import { datetimeLocal, datetimeISO } from 'utils/functions/datetime'
import { paidTextError } from 'utils/functions/price'
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
import BlogModal from 'components/widgets/Modal/Blog'
import PaidTextInput from 'components/widgets/PaidTextInput'
import TextEditor from 'components/widgets/TextEditor'
import style from '../../Form.module.scss'

interface Props {
  channels: Channel[]
  categories: Category[]
  seller: PaymentSellerOut
  data: Blog
}

export default function ManageBlogEdit(props: Props): React.JSX.Element {
  const { channels, categories, seller, data } = props
  const { categoryUlid, title, content, richtext, paidText, publish, publishAt, isPromotion } = data
  const price = data.product?.price.amount ?? 0
  const currency = data.product?.price.currency ?? seller.currency

  const router = useRouter()
  const { t } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { error, validate } = useRequired()
  const { toast, handleToast } = useToast()
  const [isModal, setIsModal] = useState<boolean>(false)
  const [isSale, setIsSale] = useState<boolean>(paidText !== '')
  const [values, setValues] = useState<BlogUpdateIn>({ categoryUlid, title, content, richtext, paidText, price, publish, isPromotion, publishAt: datetimeISO(publishAt) })

  const channelOptions = channels.map((c) => ({ label: c.name, value: c.ulid }))
  const categoryOptions = [{ label: t('manage.form.unselected'), value: '' }, ...categories.map((c) => ({ label: c.jpName, value: c.ulid }))]

  const handleBack = () => router.push('/manage/blog')
  const handleModal = () => setIsModal(!isModal)
  const handleSelect = (e: ChangeEvent<HTMLSelectElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleFile = (file: File) => setValues({ ...values, image: file })
  const handlePromotion = () => setValues({ ...values, isPromotion: !values.isPromotion })
  const handlePublish = () => setValues({ ...values, publish: !values.publish })
  const handlePublishAt = (publishAt: string) => setValues({ ...values, publishAt: datetimeISO(publishAt) })
  const handleSale = () => setIsSale(!isSale)
  const handlePaidText = (paidText: string) => setValues({ ...values, paidText })
  const handlePrice = (price: number) => setValues({ ...values, price })

  const handleRichtext = (html: string) => {
    const richtext = html.trim() === '<p></p>' ? '' : html.trim()
    setValues({ ...values, richtext })
  }

  const handleForm = async () => {
    const { categoryUlid, title, content, richtext } = values
    if (!validate({ categoryUlid, title, content, richtext })) return
    const paidError = isSale ? paidTextError(values.paidText, values.price) : ''
    if (paidError !== '') {
      handleToast(paidError, true)
      return
    }
    const request = isSale ? values : { ...values, paidText: '', price: 0 }
    handleLoading(true)
    const ret = await putManageBlog(data.ulid, request)
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
    <Main title="Blog" type="table" toast={toast} isFooter={false} button={button}>
      <form className={style.form} method="POST" action="">
        <VStack gap="8">
          <ToggleCard label={t('manage.form.publish')} isActive={values.publish} onClick={handlePublish} />
          <DatePicker label={t('manage.form.publishAt')} name="publishAt" value={datetimeLocal(values.publishAt)} onChange={handlePublishAt} isTime />
          <ToggleCard label={t('manage.form.promotion')} isActive={values.isPromotion} onClick={handlePromotion} />
          <SelectBox label={t('manage.form.channel')} name="channelUlid" value={data.channel.ulid} options={channelOptions} disabled />
          <SelectBox label={t('manage.form.category')} name="categoryUlid" value={values.categoryUlid} options={categoryOptions} required error={error} onChange={handleSelect} />
          <Input label={t('manage.form.title')} name="title" maxLength={100} value={values.title} required error={error} onChange={handleInput} />
          <Textarea label={t('manage.form.content')} name="content" value={values.content} required error={error} onChange={handleText} />
          <InputFile label={t('manage.form.thumbnail')} accept="image/*" required error={error} onChange={handleFile} />
          <TextEditor label={t('manage.form.richtext')} value={values.richtext} required error={error} onChange={handleRichtext} />
          <PaidTextInput
            isSale={isSale}
            paidText={values.paidText}
            price={values.price}
            currency={currency}
            isAvailable={seller.isAvailable || paidText !== ''}
            isEnabled={seller.isEnabled || paidText !== ''}
            onSale={handleSale}
            onPaidText={handlePaidText}
            onPrice={handlePrice}
          />
        </VStack>
      </form>
      <BlogModal open={isModal} onClose={handleModal} richtext={values.richtext} paidText={isSale ? values.paidText : ''} isPromotion={values.isPromotion} />
    </Main>
  )
}
