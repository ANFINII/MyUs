import { HomeMedia, Search } from 'types/internal/media'
import Main from 'components/layout/Main'

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
        {/* {videos?.map((data) => (
          <ArticleVideo data={data} key={data.id} />
        ))} */}
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
    </Main>
  )
}
