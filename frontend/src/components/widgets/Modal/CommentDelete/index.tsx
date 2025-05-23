import Modal from 'components/parts/Modal'

export interface Props {
  open: boolean
  onClose: () => void
  onAction: () => void
  loading?: boolean
  content: React.ReactNode
}

export default function CommentDeleteModal(props: Props): JSX.Element {
  const { open, onClose, onAction, loading, content } = props

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="メッセージの削除"
      actions={[{ name: '削除', color: 'red', loading, onClick: onAction }, { name: 'キャンセル', color: 'white', onClick: onClose }]}
    >
      <div>このメッセージを削除しますか？</div>
      {content}
    </Modal>
  )
}
