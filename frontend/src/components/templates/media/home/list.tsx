import { MediaHome, Search } from 'types/internal/media'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import MediaBlog from 'components/widgets/Media/Index/Blog'
import MediaChat from 'components/widgets/Media/Index/Chat'
import MediaComic from 'components/widgets/Media/Index/Comic'
import MediaMusic from 'components/widgets/Media/Index/Music'
import MediaPicture from 'components/widgets/Media/Index/Picture'
import MediaVideo from 'components/widgets/Media/Index/Video'
import MediaIndex from 'components/widgets/Media/List/Index'

interface Props {
  mediaHome: MediaHome
  search?: Search
}

export default function Homes(props: Props): React.JSX.Element {
  const { mediaHome, search } = props
  const { videos, musics, comics, pictures, blogs, chats } = mediaHome

  return (
    <Main title="Home" search={search}>
      <Divide />
      <MediaIndex title="Video">
        {videos?.map((media) => (
          <MediaVideo key={media.ulid} media={media} />
        ))}
      </MediaIndex>

      <Divide />
      <MediaIndex title="Music">
        {musics?.map((media) => (
          <MediaMusic key={media.ulid} media={media} />
        ))}
      </MediaIndex>

      <Divide />
      <MediaIndex title="Comic">
        {comics?.map((media) => (
          <MediaComic key={media.ulid} media={media} />
        ))}
      </MediaIndex>

      <Divide />
      <MediaIndex title="Picture">
        {pictures?.map((media) => (
          <MediaPicture key={media.ulid} media={media} />
        ))}
      </MediaIndex>

      <Divide />
      <MediaIndex title="Blog">
        {blogs?.map((media) => (
          <MediaBlog key={media.ulid} media={media} />
        ))}
      </MediaIndex>

      <Divide />
      <MediaIndex title="Chat">
        {chats?.map((media) => (
          <MediaChat key={media.ulid} media={media} />
        ))}
      </MediaIndex>
    </Main>
  )
}
