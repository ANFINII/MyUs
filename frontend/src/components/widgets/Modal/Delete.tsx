import { useTranslation } from 'react-i18next'
import Modal from 'components/parts/Modal'

interface Props {
  open: boolean
  title: string
  content: string
  loading?: boolean
  onClose: () => void
  onAction: () => void
}

export default function DeleteModal(props: Props): React.JSX.Element {
  const { open, title, content, loading, onClose, onAction } = props

  const { t } = useTranslation()

  return (
    <Modal
      open={open}
      onClose={onClose}
      title={title}
      actions={[
        { name: t('action.delete'), color: 'red', loading, onClick: onAction },
        { name: t('action.cancel'), color: 'white', onClick: onClose },
      ]}
    >
      <div>{content}</div>
    </Modal>
  )
}
