import {Query, VideoResponse} from 'utils/type'
import Main from 'components/layouts/Main'
import ArticleVideo from 'components/elements/Article/Video'
import ArticleMusic from 'components/elements/Article/Music'
import ArticlePicture from 'components/elements/Article/Picture'
import ArticleBlog from 'components/elements/Article/Blog'
import ArticleChat from 'components/elements/Article/Chat'

interface Props {
  query?: Query
  datas: Array<VideoResponse>
}

export default function HomeList(props: Props) {
  const {query, datas} = props
  return (
    <Main title="MyUsホームページ" hero="Home" query={query}>
      <hr/>

      <article className="article_index">
        <h2>Video</h2>
        {/* {% if query %} */}
          {/* {% include 'search/search_video.html' %} */}
        {/* {% else %} */}
          <ArticleVideo datas={datas} />
        {/* {% endif %} */}
      </article>
      <hr/>

      <article className="article_index">
        <h2>Music</h2>
        {/* {% if query %} */}
          {/* {% include 'search/search_music.html' %} */}
        {/* {% else %} */}
          {/* {% for item in music_list %} */}
            {/* <ArticleMusic imageUrl={music} /> */}
          {/* {% endfor %} */}
        {/* {% endif %} */}
      </article>
      <hr/>

      <article className="article_index">
        <h2>Picture</h2>
        {/* {% if query %} */}
          {/* {% include 'search/search_picture.html' %} */}
        {/* {% else %} */}
          {/* {% for item in picture_list %} */}
            {/* <ArticlePicture imageUrl='/user_icon.png' /> */}
          {/* {% endfor %} */}
        {/* {% endif %} */}
      </article>
      <hr/>

      <article className="article_index">
        <h2>Blog</h2>
        {/* {% if query %} */}
          {/* {% include 'search/search_blog.html' %} */}
        {/* {% else %} */}
          {/* {% for item in blog_list %} */}
            {/* <ArticleBlog imageUrl='/user_icon.png' /> */}
          {/* {% endfor %} */}
        {/* {% endif %} */}
      </article>
      <hr/>

      <article className="article_index">
        <h2>Chat</h2>
        {/* {% if query %} */}
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
