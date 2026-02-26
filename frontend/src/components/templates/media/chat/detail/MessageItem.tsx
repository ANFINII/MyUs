import { useState, useRef } from 'react'
import { ChatMessage } from 'types/internal/media/detail'
import { UserMe } from 'types/internal/user'
import { formatDatetime } from 'utils/functions/datetime'
import ActionList, { ActionItem } from 'components/parts/ActionList'
import AvatarLink from 'components/parts/Avatar/Link'
import IconDots from 'components/parts/Icon/Dots'
import IconEdit from 'components/parts/Icon/Edit'
import IconTrash from 'components/parts/Icon/Trash'
import Modal from 'components/parts/Modal'
import ChatEditor from './ChatEditor'
import style from './detail.module.scss'

interface Props {
  user?: UserMe
  message: ChatMessage
  isDisabled?: boolean
  onThread?: (message: ChatMessage) => void
  onEdit?: (ulid: string, text: string) => void
  onDelete?: (ulid: string) => void
}

export default function MessageItem(props: Props): React.JSX.Element {
  const { user, message, isDisabled = false, onThread, onEdit, onDelete } = props

  const [isMenu, setIsMenu] = useState<boolean>(false)
  const [isEdit, setIsEdit] = useState<boolean>(false)
  const [isModal, setIsModal] = useState<boolean>(false)
  const [editText, setEditText] = useState<string>(message.text)
  const actionRef = useRef<HTMLButtonElement>(null)

  const isOwner = user !== undefined && message.author.ulid === user.ulid
  const disabled = !isOwner || isDisabled

  const handleMenu = () => setIsMenu(!isMenu)
  const handleModal = () => setIsModal(!isModal)

  const handleEditStart = () => {
    setEditText(message.text)
    setIsEdit(true)
  }

  const handleEditSubmit = () => {
    if (editText.replace(/<[^>]*>/g, '').trim().length === 0) return
    onEdit?.(message.ulid, editText)
    setIsEdit(false)
  }

  const handleEditCancel = () => setIsEdit(false)

  const handleDelete = () => {
    onDelete?.(message.ulid)
    setIsModal(false)
  }

  const actionItems: ActionItem[] = [
    { icon: <IconEdit size="16" />, label: '編集', onClick: handleEditStart },
    { icon: <IconTrash size="16" />, label: '削除', onClick: handleModal, danger: true },
  ]

  return (
    <div className={style.message_item}>
      <AvatarLink src={message.author.avatar} size="m" ulid={message.author.ulid} nickname={message.author.nickname} />
      <div className={style.message_content}>
        <div className={style.message_meta}>
          <p>{message.author.nickname}</p>
          <time>{formatDatetime(message.created)}</time>
        </div>
        {isEdit ? (
          <div className={style.message_edit}>
            <ChatEditor value={editText} onChange={setEditText} />
            <div className={style.message_edit_actions}>
              <button className={style.edit_cancel} onClick={handleEditCancel}>
                キャンセル
              </button>
              <button className={style.edit_save} onClick={handleEditSubmit}>
                保存
              </button>
            </div>
          </div>
        ) : (
          <div className={style.message_text} dangerouslySetInnerHTML={{ __html: message.text }} />
        )}
        {onThread && !isEdit && (
          <div className={style.message_thread_link} onClick={() => onThread(message)}>
            スレッド表示
          </div>
        )}
      </div>
      {onEdit && onDelete && (
        <div className={style.message_action}>
          <button ref={actionRef} className={style.action_button} disabled={disabled} onClick={handleMenu}>
            <IconDots size="18" />
          </button>
          <div className={style.action_list}>
            <ActionList triggerRef={actionRef} open={isMenu} onClose={handleMenu} items={actionItems} />
          </div>
        </div>
      )}
      <Modal
        open={isModal}
        onClose={handleModal}
        title="メッセージの削除"
        actions={[
          { name: '削除', color: 'red', onClick: handleDelete },
          { name: 'キャンセル', color: 'white', onClick: handleModal },
        ]}
      >
        <p>このメッセージを削除しますか？</p>
      </Modal>
    </div>
  )
}
