import {GetServerSideProps} from 'next'
import Head from 'next/head'
import VideoArticle from 'components/elements/Article/Video'


interface author {
  id: number
  nickname: string
  image: string
}

export interface MediaResponse {
  id: number
  title: string
  content: string
  // hashtag: string
  like: number
  read: number
  comment_num: number
  publish: boolean
  created: string
  updated: string
  // totalLike: number
  author: author
}

export interface VideoResponse extends MediaResponse {
  image: string
  video: string
  convert: string
}

interface Props {
  query: string
  count: number
}

export async function getVideoList() {
  const BASEURL = process.env.NEXT_PUBLIC_API_URL
  const res = await fetch(BASEURL + '/api/video')
  const data = await res.json()
  return data
}

export const getServerSideProps: GetServerSideProps = async () => {
  const data = await getVideoList()
  return {
    props: { data },
  }
}

export default function Video(props: Props) {
  const {query, count} = props

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
        <title>MyUsビデオ</title>
      </Head>

      <h1>Video
        {query &&
          <section className="search_message">
            「{query}」の検索結果「{count}」件
          </section>
        }
      </h1>

      <VideoArticle videos={datas} />

      {/* {% block extrajs %}
      <script src="https://vjs.zencdn.net/7.19.2/video.min.js"></script>
      <script src="{% static 'js/video_auto.js' %}"></script>
      {% endblock extrajs %}     */}
    </>
  )
}
