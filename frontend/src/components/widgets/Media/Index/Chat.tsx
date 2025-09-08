import { Chat } from 'types/internal/media'
import ChatMediaContent from 'components/widgets/Media/Content/Chat'
import style from './Media.module.scss'

interface Props {
  media: Chat
}

export default function MediaChat(props: Props): React.JSX.Element {
  const { media } = props
  const { id } = media

  return (
    <section className={style.media_chat}>
      <ChatMediaContent href={`/media/chat/${id}`} media={media} />
    </section>
  )
}
