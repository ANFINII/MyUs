import { HomeMedia, Search } from 'types/internal/media'
import Main from 'components/layout/Main'
import ArticleBlog from 'components/widgets/Article/Blog'
import ArticleChat from 'components/widgets/Article/Chat'
import ArticleComic from 'components/widgets/Article/Comic'
import ArticleMusic from 'components/widgets/Article/Music'
import ArticlePicture from 'components/widgets/Article/Picture'
import ArticleVideo from 'components/widgets/Article/Video'

interface Props {
  homeMedia: HomeMedia
  search?: Search
}

export default function Homes(props: Props) {
  const { search, homeMedia } = props
  const { videos, musics, comics, pictures, blogs, chats } = homeMedia

  return (
    <Main title="Home" search={search}>
      <hr />

      <article className="article_index">
        <h2>Video</h2>
        {videos?.map((data) => (
          <ArticleVideo key={data.id} data={data} />
        ))}
      </article>
      <hr />

      <article className="article_index">
        <h2>Music</h2>
        {musics?.map((data) => (
          <ArticleMusic key={data.id} data={data} />
        ))}
      </article>
      <hr />

      <article className="article_index">
        <h2>Comic</h2>
        {comics?.map((data) => (
          <ArticleComic key={data.id} data={data} />
        ))}
      </article>
      <hr />

      <article className="article_index">
        <h2>Picture</h2>
        {pictures?.map((data) => (
          <ArticlePicture key={data.id} data={data} />
        ))}
      </article>
      <hr />

      <article className="article_index">
        <h2>Blog</h2>
        {blogs?.map((data) => (
          <ArticleBlog key={data.id} data={data} />
        ))}
      </article>
      <hr />

      <article className="article_index">
        <h2>Chat</h2>
        {chats?.map((data) => (
          <ArticleChat key={data.id} data={data} />
        ))}
      </article>
    </Main>
  )
}
