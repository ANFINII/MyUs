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

  return (
    <Modal
      open={open}
      onClose={onClose}
      title={title}
      actions={[
        { name: '削除', color: 'red', loading, onClick: onAction },
        { name: 'キャンセル', color: 'white', onClick: onClose },
      ]}
    >
      <div>{content}</div>
    </Modal>
  )
}
