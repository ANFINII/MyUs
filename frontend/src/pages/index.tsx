// import axios from 'pages/api/axios'
import { GetServerSideProps } from 'next'
import { HomeMedia, Search } from 'types/internal/media'
import Homes from 'components/templates/media/home/list'

export const getServerSideProps: GetServerSideProps = async () => {
  // const res_video = await axios.get('/api/video')
  // const video: any = res_video.data
  // const res_music = await axios.get('/api/music')
  // const music: any = res_music.data

  const search: Search = {
    name: 'test',
    count: 0,
  }

  const homeMedia: HomeMedia = {
    videos: [
      {
        id: 1,
        title: '動画テスト1',
        content: '動画テスト1',
        image: '/',
        video: '/media/videos/videos_video/user_1/object_1/m001.mp4',
        convert: '/media/videos/videos_video/user_1/object_1/m001.mp4',
        like: 0,
        read: 101,
        commentCount: 0,
        publish: true,
        created: '2023-01-01T00:00:00Z',
        updated: '2023-01-01T00:00:00Z',
        author: {
          id: 1,
          nickname: 'アンさん',
          image: '/',
        },
        modelName: 'video',
      },
      {
        id: 2,
        title: '動画テスト2',
        content: '動画テスト2',
        image: '/',
        video: '/media/videos/videos_video/user_1/object_1/m001.mp4',
        convert: '/media/videos/videos_video/user_1/object_1/m001.mp4',
        like: 0,
        read: 100,
        commentCount: 0,
        publish: true,
        created: '2023-01-01T00:00:00Z',
        updated: '2023-01-01T00:00:00Z',
        author: {
          id: 2,
          nickname: 'ショウエン',
          image: '/',
        },
        modelName: 'video',
      },
      {
        id: 3,
        title: '動画テスト3',
        content: '動画テスト3',
        image: '/',
        video: '/media/videos/videos_video/user_1/object_1/m001.mp4',
        convert: '/media/videos/videos_video/user_1/object_1/m001.mp4',
        like: 0,
        read: 100,
        commentCount: 0,
        publish: true,
        created: '2023-01-01T00:00:00Z',
        updated: '2023-01-01T00:00:00Z',
        author: {
          id: 3,
          nickname: 'ソウヒ',
          image: '/',
        },
        modelName: 'video',
      },
      {
        id: 4,
        title: '動画テスト4',
        content: '動画テスト4',
        image: '/',
        video: '/media/videos/videos_video/user_1/object_1/m001.mp4',
        convert: '/media/videos/videos_video/user_1/object_1/m001.mp4',
        like: 0,
        read: 100,
        commentCount: 0,
        publish: true,
        created: '2023-01-01T00:00:00Z',
        updated: '2023-01-01T00:00:00Z',
        author: {
          id: 4,
          nickname: 'ケイマ',
          image: '/',
        },
        modelName: 'video',
      },
      {
        id: 5,
        title: '動画テスト5',
        content: '動画テスト5',
        image: '/',
        video: '/media/videos/videos_video/user_1/object_1/m001.mp4',
        convert: '/media/videos/videos_video/user_1/object_1/m001.mp4',
        like: 0,
        read: 100,
        commentCount: 0,
        publish: true,
        created: '2023-01-01T00:00:00Z',
        updated: '2023-01-01T00:00:00Z',
        author: {
          id: 5,
          nickname: 'アン',
          image: '/',
        },
        modelName: 'video',
      },
    ],
    musics: [],
    comics: [],
    pictures: [],
    blogs: [],
    chats: [],
  }

  return { props: { homeMedia } }
}

interface Props {
  homeMedia: HomeMedia
  search?: Search
}

export default function HomesPage(props: Props) {
  return <Homes {...props} />
}

{
  /* <Script src="https://vjs.zencdn.net/7.19.2/video.min.js"></Script>
<Script src='/pages/api/video_auto.js'></Script>
<script>$(function() { $('audio').audioPlayer() })</cript> */
}
