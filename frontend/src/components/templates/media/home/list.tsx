import { MediaHome } from 'types/internal/media'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import MediaBlog from 'components/widgets/Media/Index/Blog'
import MediaChat from 'components/widgets/Media/Index/Chat'
import MediaComic from 'components/widgets/Media/Index/Comic'
import MediaIndex from 'components/widgets/Media/Index/Index'
import MediaMusic from 'components/widgets/Media/Index/Music'
import MediaPicture from 'components/widgets/Media/Index/Picture'
import MediaVideo from 'components/widgets/Media/Index/Video'

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
      <MediaIndex title="Video">
        {videos?.map((media) => (
          <MediaVideo key={media.ulid} data={media} />
        ))}
      </MediaIndex>

      <Divide />
      <MediaIndex title="Music">
        {musics?.map((media) => (
          <MediaMusic key={media.ulid} data={media} />
        ))}
      </MediaIndex>

      <Divide />
      <MediaIndex title="Comic">
        {comics?.map((media) => (
          <MediaComic key={media.ulid} data={media} />
        ))}
      </MediaIndex>

      <Divide />
      <MediaIndex title="Picture">
        {pictures?.map((media) => (
          <MediaPicture key={media.ulid} data={media} />
        ))}
      </MediaIndex>

      <Divide />
      <MediaIndex title="Blog">
        {blogs?.map((media) => (
          <MediaBlog key={media.ulid} data={media} />
        ))}
      </MediaIndex>

      <Divide />
      <MediaIndex title="Chat">
        {chats?.map((media) => (
          <MediaChat key={media.ulid} data={media} />
        ))}
      </MediaIndex>
    </Main>
  )
}
