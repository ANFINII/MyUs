import type { NextPage } from 'next'
import Head from 'next/head'
import VideoArticle from 'components/elements/article/video'
import MusicArticle from 'components/elements/article/music'
import PictureArticle from 'components/elements/article/picture'
import BlogArticle from 'components/elements/article/blog'
import ChatArticle from 'components/elements/article/chat'

const Home: NextPage = () => {
  return (
    <>
      <Head>
        <title>MyUsホームページ</title>
      </Head>

      <h1>Recommend
        {/* {% if Recommend %}{{ Recommend }}{% else %}Home{% endif %} */}
        {/* {% if query %} */}
        {/* <section className="messages_search">「{{ query }}」の検索結果「{{ count }}」件</section> */}
        {/* {% endif %} */}
      </h1>
      <hr/>

      <article className="main_article_index">
        <h2>Video</h2>
        {/* {% if query %} */}
          {/* {% include 'search/search_video.html' %} */}
        {/* {% else %} */}
          {/* {% for item in video_list %} */}
            <VideoArticle/>
          {/* {% endfor %} */}
        {/* {% endif %} */}
      </article>
      <hr/>

      <article className="main_article_index">
        <h2>Live</h2>
        {/* {% if query %}
          {% include 'search/search_live.html' %}
        {% else %}
          {% for item in live_list %}
            <LiveArticle/>
          {% endfor %}
        {% endif %} */}
      </article>
      <hr/>

      <article className="main_article_index">
        <h2>Music</h2>
        {/* {% if query %} */}
          {/* {% include 'search/search_music.html' %} */}
        {/* {% else %} */}
          {/* {% for item in music_list %} */}
            <MusicArticle/>
          {/* {% endfor %} */}
        {/* {% endif %} */}
      </article>
      <hr/>

      <article className="main_article_index">
        <h2>Picture</h2>
        {/* {% if query %} */}
          {/* {% include 'search/search_picture.html' %} */}
        {/* {% else %} */}
          {/* {% for item in picture_list %} */}
            <PictureArticle/>
          {/* {% endfor %} */}
        {/* {% endif %} */}
      </article>
      <hr/>

      <article className="main_article_index">
        <h2>Blog</h2>
        {/* {% if query %} */}
          {/* {% include 'search/search_blog.html' %} */}
        {/* {% else %} */}
          {/* {% for item in blog_list %} */}
            <BlogArticle/>
          {/* {% endfor %} */}
        {/* {% endif %} */}
      </article>
      <hr/>

      <article className="main_article_index">
        <h2>Chat</h2>
        {/* {% if query %} */}
          {/* {% include 'search/search_chat.html' %} */}
        {/* {% else %} */}
          {/* {% for item in chat_list %} */}
            <ChatArticle/>
          {/* {% endfor %} */}
        {/* {% endif %} */}
      </article>

      <script src="https://vjs.zencdn.net/7.19.2/video.min.js"></script>
      <script src='/pages/api/video_auto.js'></script>
      {/* <script>$(function() { $('audio').audioPlayer(); });</script> */}
    </>
  )
}
export default Home
