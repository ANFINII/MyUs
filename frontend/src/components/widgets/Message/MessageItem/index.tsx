import { useState } from 'react'
import { useRouter } from 'next/router'
import { ChatMessage } from 'types/internal/media/output'
import { UserMe } from 'types/internal/user'
import cx from 'utils/functions/cx'
import { formatDatetime } from 'utils/functions/datetime'
import ActionButton from 'components/parts/Action/Button'
import { ActionItem } from 'components/parts/Action/List'
import AvatarLink from 'components/parts/Avatar/Link'
import IconEdit from 'components/parts/Icon/Edit'
import IconLink from 'components/parts/Icon/Link'
import IconTrash from 'components/parts/Icon/Trash'
import HStack from 'components/parts/Stack/Horizontal'
import MessageDeleteModal from 'components/widgets/Modal/MessageDelete'
import style from './MessageItem.module.scss'
import ChatEditor from '../ChatEditor'

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

  const router = useRouter()
  const [isMenu, setIsMenu] = useState<boolean>(false)
  const [isEdit, setIsEdit] = useState<boolean>(false)
  const [isModal, setIsModal] = useState<boolean>(false)
  const [editText, setEditText] = useState<string>(message.text)

  const chatUlid = String(router.query.ulid)
  const threadPath = `/media/chat/${chatUlid}/thread/${message.ulid}`
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
    navigator.clipboard.writeText(`${window.location.origin}${threadPath}`)
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
      <AvatarLink src={message.author.avatar} ulid={message.author.ulid} title={message.author.nickname} />
      <div className={style.message_content}>
        <div className={style.message_meta}>
          <p>{message.author.nickname}</p>
          <time>{formatDatetime(message.created)}</time>
        </div>
        {isEdit ? (
          <ChatEditor value={editText} onChange={setEditText} onCancel={handleEditCancel} onSave={handleEditSubmit} />
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
      <div className={cx(style.message_action, isMenu && style.visible)}>
        <ActionButton open={isMenu} onMenu={handleMenu} actionItems={actionItems} />
      </div>
      <MessageDeleteModal open={isModal} onClose={handleModal} onAction={handleDelete} message={message} />
    </div>
  )
}
