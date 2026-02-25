import { ChatMessage } from 'types/internal/media/detail'
import { formatDatetime } from 'utils/functions/datetime'
import AvatarLink from 'components/parts/Avatar/Link'
import style from './detail.module.scss'

interface Props {
  message: ChatMessage
  onThreadToggle?: (message: ChatMessage) => void
}

export default function MessageItem(props: Props): React.JSX.Element {
  const { message, onThreadToggle } = props

  return (
    <div className={style.message_item}>
      <AvatarLink src={message.author.avatar} size="m" ulid={message.author.ulid} nickname={message.author.nickname} />
      <div className={style.message_content}>
        <div className={style.message_meta}>
          <p>{message.author.nickname}</p>
          <time>{formatDatetime(message.created)}</time>
        </div>
        <div className={style.message_text} dangerouslySetInnerHTML={{ __html: message.text }} />
        {onThreadToggle && (
          <div className={style.message_thread_link} onClick={() => onThreadToggle(message)}>
            スレッド表示
          </div>
        )}
      </div>
    </div>
  )
}
