import { useState } from 'react'
import clsx from 'clsx'
import { ChatMessage } from 'types/internal/media/detail'
import { UserMe } from 'types/internal/user'
import { formatDatetime } from 'utils/functions/datetime'
import ActionButton from 'components/parts/Action/Button'
import { ActionItem } from 'components/parts/Action/List'
import AvatarLink from 'components/parts/Avatar/Link'
import IconEdit from 'components/parts/Icon/Edit'
import IconLink from 'components/parts/Icon/Link'
import IconTrash from 'components/parts/Icon/Trash'
import Modal from 'components/parts/Modal'
import HStack from 'components/parts/Stack/Horizontal'
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

  const isOwner = user !== undefined && message.author.ulid === user.ulid

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

  const handleCopyLink = () => {
    const url = `${window.location.origin}${window.location.pathname}`
    navigator.clipboard.writeText(url)
  }

  const actionItems: ActionItem[] = [
    { icon: <IconLink size="16" />, label: 'コピー', onClick: handleCopyLink },
    ...(isOwner && !isDisabled
      ? [
          { icon: <IconEdit size="16" />, label: '編集', onClick: handleEditStart },
          { icon: <IconTrash size="16" />, label: '削除', onClick: handleModal, danger: true },
        ]
      : []),
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
          <div className={style.message_thread_row}>
            <span className={style.message_thread_link} onClick={() => onThread(message)}>
              スレッド表示
            </span>
            <HStack gap="1" className={style.message_thread_count}>
              <span>返信</span>
              <span>{message.replyCount}</span>
              <span>件</span>
            </HStack>
          </div>
        )}
      </div>
      <div className={clsx(style.message_action, isMenu && style.visible)}>
        <ActionButton open={isMenu} onMenu={handleMenu} actionItems={actionItems} />
      </div>
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
