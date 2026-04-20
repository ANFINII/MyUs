import { MediaHome } from 'types/internal/media/output'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import CardIndexList from 'components/widgets/Card/IndexList'
import BlogCard from 'components/widgets/Card/Media/Blog'
import ChatCard from 'components/widgets/Card/Media/Chat'
import ComicCard from 'components/widgets/Card/Media/Comic'
import MusicCard from 'components/widgets/Card/Media/Music'
import PictureCard from 'components/widgets/Card/Media/Picture'
import VideoCard from 'components/widgets/Card/Media/Video'

interface Props {
  title: string
  mediaHome: MediaHome
}

export default function Homes(props: Props): React.JSX.Element {
  const { title, mediaHome } = props
  const { videos, musics, comics, pictures, blogs, chats } = mediaHome

  const search = useSearch([videos, musics, comics, pictures, blogs, chats])

  return (
    <Main title={title} search={search}>
      <Divide />
      <CardIndexList title="Video">
        {videos?.map((media) => (
          <VideoCard key={media.ulid} item={media} />
        ))}
      </CardIndexList>

      <Divide />
      <CardIndexList title="Music">
        {musics?.map((media) => (
          <MusicCard key={media.ulid} item={media} />
        ))}
      </CardIndexList>

      <Divide />
      <CardIndexList title="Comic">
        {comics?.map((media) => (
          <ComicCard key={media.ulid} item={media} />
        ))}
      </CardIndexList>

      <Divide />
      <CardIndexList title="Picture">
        {pictures?.map((media) => (
          <PictureCard key={media.ulid} item={media} />
        ))}
      </CardIndexList>

      <Divide />
      <CardIndexList title="Blog">
        {blogs?.map((media) => (
          <BlogCard key={media.ulid} item={media} />
        ))}
      </CardIndexList>

      <Divide />
      <CardIndexList title="Chat">
        {chats?.map((media) => (
          <ChatCard key={media.ulid} item={media} />
        ))}
      </CardIndexList>
    </Main>
  )
}
