import { Search, VideoResponse } from 'types/media'
import Layout from 'components/layout'
import Main from 'components/layout/Main'
import ArticleBlog from 'components/widgets/Article/Blog'
import ArticleChat from 'components/widgets/Article/Chat'
import ArticleComic from 'components/widgets/Article/Comic'
import ArticleMusic from 'components/widgets/Article/Music'
import ArticlePicture from 'components/widgets/Article/Picture'
import ArticleVideo from 'components/widgets/Article/Video'

interface Props {
  search?: Search
  videos: VideoResponse[]
  datas?: VideoResponse[]
  // datas: VideoResponse[]
  // datas: VideoResponse[]
  // datas: VideoResponse[]
  // datas: VideoResponse[]
}

export default function Homes(props: Props) {
  const { search, datas, videos } = props

  return (
    <Layout title="Home" search={search}>
      <hr />

      <article className="article_index">
        <h2>Video</h2>
        {videos.map((data) => (
          <ArticleVideo data={data} key={data.id} />
        ))}
      </article>
      <hr />

      <article className="article_index">
        <h2>Music</h2>
        {/* {% if search %} */}
        {/* {% include 'search/search_music.html' %} */}
        {/* {% else %} */}
        {/* {% for item in music_list %} */}
        {/* <ArticleMusic imageUrl={music} /> */}
        {/* {% endfor %} */}
        {/* {% endif %} */}
      </article>
      <hr />

      <article className="article_index">
        <h2>Comic</h2>
        {/* {% if search %}
          {% include 'search/search_picture.html' %}
        {% else %}
          {% for item in comic_list %}
            {% include 'media/comic/comic_article.html' %}
          {% endfor %}
        {% endif %} */}
      </article>
      <hr />

      <article className="article_index">
        <h2>Picture</h2>
        {/* {% if search %} */}
        {/* {% include 'search/search_picture.html' %} */}
        {/* {% else %} */}
        {/* {% for item in picture_list %} */}
        {/* <ArticlePicture imageUrl='/user_icon.png' /> */}
        {/* {% endfor %} */}
        {/* {% endif %} */}
      </article>
      <hr />

      <article className="article_index">
        <h2>Blog</h2>
        {/* {% if search %} */}
        {/* {% include 'search/search_blog.html' %} */}
        {/* {% else %} */}
        {/* {% for item in blog_list %} */}
        {/* <ArticleBlog imageUrl='/user_icon.png' /> */}
        {/* {% endfor %} */}
        {/* {% endif %} */}
      </article>
      <hr />

      <article className="article_index">
        <h2>Chat</h2>
        {/* {% if search %} */}
        {/* {% include 'search/search_chat.html' %} */}
        {/* {% else %} */}
        {/* {% for item in chat_list %} */}
        {/* <ArticleChat/> */}
        {/* {% endfor %} */}
        {/* {% endif %} */}
      </article>
    </Layout>
  )
}
