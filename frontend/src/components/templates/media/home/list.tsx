import { MediaHome } from 'types/internal/media'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import BlogCard from 'components/widgets/Card/Blog'
import ChatCard from 'components/widgets/Card/Chat'
import ComicCard from 'components/widgets/Card/Comic'
import CardIndexList from 'components/widgets/Card/IndexList'
import MusicCard from 'components/widgets/Card/Music'
import PictureCard from 'components/widgets/Card/Picture'
import VideoCard from 'components/widgets/Card/Video'

interface Props {
  mediaHome: MediaHome
}

export default function Homes(props: Props): React.JSX.Element {
  const { mediaHome } = props
  const { videos, musics, comics, pictures, blogs, chats } = mediaHome

  const search = useSearch([videos, musics, comics, pictures, blogs, chats])

  return (
    <Main title="Home" search={search}>
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
