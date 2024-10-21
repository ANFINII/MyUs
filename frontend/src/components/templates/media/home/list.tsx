import { MediaHome, Search } from 'types/internal/media'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import ArticleIndex from 'components/widgets/Media/Article/Index'
import SectionBlog from 'components/widgets/Media/Section/Blog'
import SectionChat from 'components/widgets/Media/Section/Chat'
import SectionComic from 'components/widgets/Media/Section/Comic'
import SectionMusic from 'components/widgets/Media/Section/Music'
import SectionPicture from 'components/widgets/Media/Section/Picture'
import SectionVideo from 'components/widgets/Media/Section/Video'

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

      <ArticleIndex title="Video">
        {videos?.map((data) => (
          <SectionVideo key={data.id} data={data} />
        ))}
      </ArticleIndex>

      <ArticleIndex title="Music">
        {musics?.map((data) => (
          <SectionMusic key={data.id} data={data} />
        ))}
      </ArticleIndex>

      <ArticleIndex title="Comic">
        {comics?.map((data) => (
          <SectionComic key={data.id} data={data} />
        ))}
      </ArticleIndex>

      <ArticleIndex title="Picture">
        {pictures?.map((data) => (
          <SectionPicture key={data.id} data={data} />
        ))}
      </ArticleIndex>

      <ArticleIndex title="Blog">
        {blogs?.map((data) => (
          <SectionBlog key={data.id} data={data} />
        ))}
      </ArticleIndex>

      <ArticleIndex title="Chat" divide={false}>
        {chats?.map((data) => (
          <SectionChat key={data.id} data={data} />
        ))}
      </ArticleIndex>
    </Main>
  )
}
