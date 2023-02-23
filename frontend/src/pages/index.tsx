import { NextPage, GetServerSideProps } from 'next'
import Head from 'next/head'
import Script from 'next/script'
// import axios from 'pages/api/axios'
import ArticleVideo from 'components/elements/Article/Video'
import ArticleMusic from 'components/elements/Article/Music'
import ArticlePicture from 'components/elements/Article/Picture'
import ArticleBlog from 'components/elements/Article/Blog'
import ArticleChat from 'components/elements/Article/Chat'

// export const getServerSideProps: GetServerSideProps = async () => {
//   const res_video = await axios.get('/api/video')
//   const video: any = res_video.data
//   const res_music = await axios.get('/api/music')
//   const music: any = res_music.data
//   return {
//     props: { video, music }
//   }
// }

const Home: NextPage = (video: any, music: any) => {

  const datas: Array<VideoResponse> = [
    {
      "id": 1,
      "title": "動画テスト1",
      "content": "動画テスト1",
      "image": "/media/images/images_video/user_1/object_1/001.jpg",
      "video": "/media/videos/videos_video/user_1/object_1/m001.mp4",
      "convert": "/media/videos/videos_video/user_1/object_1/m001.mp4",
      "like": 0,
      "read": 101,
      "comment_num": 0,
      "publish": true,
      "created": "2022-01-01T00:00:00Z",
      "updated": "2022-01-01T00:00:00Z",
      "author": {
        "id": 1,
        "nickname": "アンさん",
        "image": "/media/users/images_user/user_1/An_Okina.jpg"
      }
    },
    {
      "id": 2,
      "title": "動画テスト2",
      "content": "動画テスト2",
      "image": "/media/images/images_video/user_1/object_1/002.jpg",
      "video": "/media/videos/videos_video/user_1/object_1/m001.mp4",
      "convert": "/media/videos/videos_video/user_1/object_1/m001.mp4",
      "like": 0,
      "read": 100,
      "comment_num": 0,
      "publish": true,
      "created": "2022-01-01T00:00:00Z",
      "updated": "2022-01-01T00:00:00Z",
      "author": {
        "id": 2,
        "nickname": "ショウエン",
        "image": "/media/users/images_user/user_2/MyUs_Profile_02.jpg"
      }
    },
    {
      "id": 3,
      "title": "動画テスト3",
      "content": "動画テスト3",
      "image": "/media/images/images_video/user_1/object_1/003.jpg",
      "video": "/media/videos/videos_video/user_1/object_1/m001.mp4",
      "convert": "/media/videos/videos_video/user_1/object_1/m001.mp4",
      "like": 0,
      "read": 100,
      "comment_num": 0,
      "publish": true,
      "created": "2022-01-01T00:00:00Z",
      "updated": "2022-01-01T00:00:00Z",
      "author": {
        "id": 3,
        "nickname": "ソウヒ",
        "image": "/media/users/images_user/user_3/MyUs_Profile_03.jpg"
      }
    },
    {
      "id": 4,
      "title": "動画テスト4",
      "content": "動画テスト4",
      "image": "/media/images/images_video/user_1/object_1/004.jpg",
      "video": "/media/videos/videos_video/user_1/object_1/m001.mp4",
      "convert": "/media/videos/videos_video/user_1/object_1/m001.mp4",
      "like": 0,
      "read": 100,
      "comment_num": 0,
      "publish": true,
      "created": "2022-01-01T00:00:00Z",
      "updated": "2022-01-01T00:00:00Z",
      "author": {
        "id": 4,
        "nickname": "ケイマ",
        "image": "/media/users/images_user/user_4/MyUs_Profile_04.jpg"
      }
    },
    {
      "id": 5,
      "title": "動画テスト5",
      "content": "動画テスト5",
      "image": "/media/images/images_video/user_1/object_1/005.jpg",
      "video": "/media/videos/videos_video/user_1/object_1/m001.mp4",
      "convert": "/media/videos/videos_video/user_1/object_1/m001.mp4",
      "like": 0,
      "read": 100,
      "comment_num": 0,
      "publish": true,
      "created": "2022-01-01T00:00:00Z",
      "updated": "2022-01-01T00:00:00Z",
      "author": {
        "id": 5,
        "nickname": "アン",
        "image": "/media/users/images_user/user_5/MyUs_Profile_01.jpg"
      }
    }
  ]


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

      <Script src="https://vjs.zencdn.net/7.19.2/video.min.js"></Script>
      <Script src='/pages/api/video_auto.js'></Script>
      {/* <script>$(function() { $('audio').audioPlayer() })</cript> */}
    </>
  )
}
export default Home
