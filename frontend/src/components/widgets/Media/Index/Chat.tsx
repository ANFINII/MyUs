import { Chat } from 'types/internal/media'
import ChatMediaContent from 'components/widgets/Common/MediaContent/Chat'
import style from './Media.module.scss'

interface Props {
  media: Chat
}

export default function MediaChat(props: Props) {
  const { media } = props
  const { id } = media

  return (
    <section className={style.media_chat}>
      <ChatMediaContent href={`/media/chat/${id}`} media={media} />
    </section>
  )
}
