import { HomeMedia, Search } from 'types/internal/media'
import Main from 'components/layout/Main'
import ArticleBlog from 'components/widgets/Article/Blog'
import ArticleChat from 'components/widgets/Article/Chat'
import ArticleComic from 'components/widgets/Article/Comic'
import ArticleIndex from 'components/widgets/Article/Index'
import ArticleMusic from 'components/widgets/Article/Music'
import ArticlePicture from 'components/widgets/Article/Picture'
import ArticleVideo from 'components/widgets/Article/Video'

interface Props {
  homeMedia: HomeMedia
  search?: Search
}

export default function Homes(props: Props) {
  const { homeMedia, search } = props
  const { videos, musics, comics, pictures, blogs, chats } = homeMedia

  return (
    <Main title="Home" search={search}>
      <hr />

      <ArticleIndex title="Video">
        {videos?.map((data) => (
          <ArticleVideo key={data.id} data={data} />
        ))}
      </ArticleIndex>

      <ArticleIndex title="Music">
        {musics?.map((data) => (
          <ArticleMusic key={data.id} data={data} />
        ))}
      </ArticleIndex>

      <ArticleIndex title="Comic">
        {comics?.map((data) => (
          <ArticleComic key={data.id} data={data} />
        ))}
      </ArticleIndex>

      <ArticleIndex title="Picture">
        {pictures?.map((data) => (
          <ArticlePicture key={data.id} data={data} />
        ))}
      </ArticleIndex>

      <ArticleIndex title="Blog">
        {blogs?.map((data) => (
          <ArticleBlog key={data.id} data={data} />
        ))}
      </ArticleIndex>

      <ArticleIndex title="Chat">
        {chats?.map((data) => (
          <ArticleChat key={data.id} data={data} />
        ))}
      </ArticleIndex>
    </Main>
  )
}
