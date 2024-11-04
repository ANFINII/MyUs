import { Chat } from 'types/internal/media'
import style from './Media.module.scss'
import ChatMediaContent from 'components/widgets/Common/MediaContent/Chat'

interface Props {
  media: Chat
}

export default function MediaChat(props: Props) {
  const { media } = props
  const { id } = media

  return (
    <section className={style.media_chat}>
      <div className={style.decolation}>
        <ChatMediaContent href={`/media/chat/${id}`} media={media} />
      </div>
    </section>
  )
}
