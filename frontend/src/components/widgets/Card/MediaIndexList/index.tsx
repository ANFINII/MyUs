import { MediaHome } from 'types/internal/media/output'
import Divide from 'components/parts/Divide'
import CardIndexList from 'components/widgets/Card/IndexList'
import BlogCard from 'components/widgets/Card/Media/Blog'
import ChatCard from 'components/widgets/Card/Media/Chat'
import ComicCard from 'components/widgets/Card/Media/Comic'
import MusicCard from 'components/widgets/Card/Media/Music'
import PictureCard from 'components/widgets/Card/Media/Picture'
import VideoCard from 'components/widgets/Card/Media/Video'

interface Props {
  media: MediaHome
}

export default function MediaIndexList(props: Props): React.JSX.Element {
  const { media } = props
  const { videos, musics, blogs, comics, pictures, chats } = media

  return (
    <>
      <CardIndexList title="Video">
        {videos.map((item) => (
          <VideoCard key={item.ulid} item={item} />
        ))}
      </CardIndexList>

      <Divide />
      <CardIndexList title="Music">
        {musics.map((item) => (
          <MusicCard key={item.ulid} item={item} items={musics} />
        ))}
      </CardIndexList>

      <Divide />
      <CardIndexList title="Blog">
        {blogs.map((item) => (
          <BlogCard key={item.ulid} item={item} />
        ))}
      </CardIndexList>

      <Divide />
      <CardIndexList title="Comic">
        {comics.map((item) => (
          <ComicCard key={item.ulid} item={item} />
        ))}
      </CardIndexList>

      <Divide />
      <CardIndexList title="Picture">
        {pictures.map((item) => (
          <PictureCard key={item.ulid} item={item} />
        ))}
      </CardIndexList>

      <Divide />
      <CardIndexList title="Chat">
        {chats.map((item) => (
          <ChatCard key={item.ulid} item={item} />
        ))}
      </CardIndexList>
    </>
  )
}
