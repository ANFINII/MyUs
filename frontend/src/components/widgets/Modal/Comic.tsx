import { useTranslation } from 'react-i18next'
import Modal from 'components/parts/Modal'
import ComicViewer from 'components/widgets/ComicViewer'

interface Props {
  open: boolean
  onClose: () => void
  pages: string[]
}

export default function ComicModal(props: Props): React.JSX.Element {
  const { open, onClose, pages } = props

  const { t } = useTranslation()

  return (
    <Modal open={open} onClose={onClose} title={t('manage.button.preview')} size="l">
      <ComicViewer pages={pages} />
    </Modal>
  )
}
