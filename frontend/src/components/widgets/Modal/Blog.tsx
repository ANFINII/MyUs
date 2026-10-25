import { useTranslation } from 'react-i18next'
import Modal from 'components/parts/Modal'
import BlogArticle from 'components/widgets/BlogArticle'

interface Props {
  open: boolean
  onClose: () => void
  richtext: string
  isPromotion: boolean
}

export default function BlogModal(props: Props): React.JSX.Element {
  const { open, onClose, richtext, isPromotion } = props

  const { t } = useTranslation()

  return (
    <Modal open={open} onClose={onClose} title={t('manage.button.preview')} size="l">
      <BlogArticle richtext={richtext} isPromotion={isPromotion} />
    </Modal>
  )
}
