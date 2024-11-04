import { MediaHome, Search } from 'types/internal/media'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import MediaIndex from 'components/widgets/Media/List/Index'
import MediaBlog from 'components/widgets/Media/Index/Blog'
import MediaChat from 'components/widgets/Media/Index/Chat'
import MediaComic from 'components/widgets/Media/Index/Comic'
import MediaMusic from 'components/widgets/Media/Index/Music'
import MediaPicture from 'components/widgets/Media/Index/Picture'
import MediaVideo from 'components/widgets/Media/Index/Video'

interface Props {
  mediaHome: MediaHome
  search?: Search
}

export default function Homes(props: Props) {
  const { mediaHome, search } = props
  const { videos, musics, comics, pictures, blogs, chats } = mediaHome

  return (
    <Main title="Home" search={search}>
      <Divide />

      <MediaIndex title="Video">
        {videos?.map((data) => (
          <MediaVideo key={data.id} data={data} />
        ))}
      </MediaIndex>

      <MediaIndex title="Music">
        {musics?.map((data) => (
          <MediaMusic key={data.id} data={data} />
        ))}
      </MediaIndex>

      <MediaIndex title="Comic">
        {comics?.map((data) => (
          <MediaComic key={data.id} data={data} />
        ))}
      </MediaIndex>

      <MediaIndex title="Picture">
        {pictures?.map((data) => (
          <MediaPicture key={data.id} data={data} />
        ))}
      </MediaIndex>

      <MediaIndex title="Blog">
        {blogs?.map((data) => (
          <MediaBlog key={data.id} data={data} />
        ))}
      </MediaIndex>

      <MediaIndex title="Chat" divide={false}>
        {chats?.map((data) => (
          <MediaChat key={data.id} data={data} />
        ))}
      </MediaIndex>
    </Main>
  )
}
