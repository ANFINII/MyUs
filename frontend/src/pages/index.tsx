import { NextPage, GetServerSideProps } from 'next'
import Head from 'next/head'
import Script from 'next/script'
import axios from 'pages/api/axios'
import VideoArticle from 'components/elements/article/video'
import MusicArticle from 'components/elements/article/music'
import PictureArticle from 'components/elements/article/picture'
import BlogArticle from 'components/elements/article/blog'
import ChatArticle from 'components/elements/article/chat'

export const getServerSideProps: GetServerSideProps = async () => {
  const res_video = await axios.get('/api/video')
  const video: any = res_video.data
  const res_music = await axios.get('/api/music')
  const music: any = res_music.data
  return {
    props: { video, music }
  }
}

const Home: NextPage = (
  video: any,
  music: any,
) => {
  return (
    <>
      <Head>
        <title>MyUsホームページ</title>
      </Head>

      <h1>Home
        {/* {% if Recommend %}{{ Recommend }}{% else %}Home{% endif %} */}
        {/* {% if query %} */}
        {/* <section className="search_message">「{{ query }}」の検索結果「{{ count }}」件</section> */}
        {/* {% endif %} */}
      </h1>
      <hr/>

      <article className="article_index">
        <h2>Video</h2>
        {/* {% if query %} */}
          {/* {% include 'search/search_video.html' %} */}
        {/* {% else %} */}
          {/* {% for item in video_list %} */}
            <VideoArticle datas={video} />
          {/* {% endfor %} */}
        {/* {% endif %} */}
      </article>
      <hr/>

      <article className="article_index">
        <h2>Music</h2>
        {/* {% if query %} */}
          {/* {% include 'search/search_music.html' %} */}
        {/* {% else %} */}
          {/* {% for item in music_list %} */}
            <MusicArticle datas={music} />
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
            <PictureArticle/>
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
            <BlogArticle/>
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
            <ChatArticle/>
          {/* {% endfor %} */}
        {/* {% endif %} */}
      </article>

      <Script src="https://vjs.zencdn.net/7.19.2/video.min.js"></Script>
      <Script src='/pages/api/video_auto.js'></Script>
      {/* <script>$(function() { $('audio').audioPlayer() })</cript> */}
    </>
  )
}
export default Home