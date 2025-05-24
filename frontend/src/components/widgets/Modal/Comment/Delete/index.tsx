import Modal from 'components/parts/Modal'

export interface Props {
  open: boolean
  onClose: () => void
  mainAction: () => void
  subAction: () => void
  children: React.ReactNode
}

export default function CommentDeleteModal(props: Props): JSX.Element {
  const { open, onClose, children, mainAction, subAction } = props

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="メッセージの削除"
      actions={[{ name: '削除', color: 'red', onClick: mainAction }, { name: 'キャンセル', color: 'white', onClick: subAction }]}
    >
      <div>このメッセージを削除しますか？</div>
      {children}
    </Modal>
  )
}
