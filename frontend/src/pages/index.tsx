import {NextPage, GetServerSideProps} from 'next'
import Script from 'next/script'
// import axios from 'pages/api/axios'
import {Query, VideoResponse} from 'utils/type'
import HomeList from 'components/pages/Media/Home/List'

// export const getServerSideProps: GetServerSideProps = async () => {
//   const res_video = await axios.get('/api/video')
//   const video: any = res_video.data
//   const res_music = await axios.get('/api/music')
//   const music: any = res_music.data
//   return {
//     props: { video, music }
//   }
// }

const query: Query = {
  name: 'test',
  count: 0,
}

const datas: Array<VideoResponse> = [
  {
    id: 1,
    title: '動画テスト1',
    content: '動画テスト1',
    image: '/media/images/images_video/user_1/object_1/001.jpg',
    video: '/media/videos/videos_video/user_1/object_1/m001.mp4',
    convert: '/media/videos/videos_video/user_1/object_1/m001.mp4',
    like: 0,
    read: 101,
    comment_count: 0,
    publish: true,
    created: '2023-01-01T00:00:00Z',
    updated: '2023-01-01T00:00:00Z',
    author: {
      id: 1,
      nickname: 'アンさん',
      image: '/media/users/images_user/user_1/An_Okina.jpg',
    },
    model_name: 'video',
  },
  {
    id: 2,
    title: '動画テスト2',
    content: '動画テスト2',
    image: '/media/images/images_video/user_1/object_1/002.jpg',
    video: '/media/videos/videos_video/user_1/object_1/m001.mp4',
    convert: '/media/videos/videos_video/user_1/object_1/m001.mp4',
    like: 0,
    read: 100,
    comment_count: 0,
    publish: true,
    created: '2023-01-01T00:00:00Z',
    updated: '2023-01-01T00:00:00Z',
    author: {
      id: 2,
      nickname: 'ショウエン',
      image: '/media/users/images_user/user_2/MyUs_Profile_02.jpg',
    },
    model_name: 'video',
  },
  {
    id: 3,
    title: '動画テスト3',
    content: '動画テスト3',
    image: '/media/images/images_video/user_1/object_1/003.jpg',
    video: '/media/videos/videos_video/user_1/object_1/m001.mp4',
    convert: '/media/videos/videos_video/user_1/object_1/m001.mp4',
    like: 0,
    read: 100,
    comment_count: 0,
    publish: true,
    created: '2023-01-01T00:00:00Z',
    updated: '2023-01-01T00:00:00Z',
    author: {
      id: 3,
      nickname: 'ソウヒ',
      image: '/media/users/images_user/user_3/MyUs_Profile_03.jpg',
    },
    model_name: 'video',
  },
  {
    id: 4,
    title: '動画テスト4',
    content: '動画テスト4',
    image: '/media/images/images_video/user_1/object_1/004.jpg',
    video: '/media/videos/videos_video/user_1/object_1/m001.mp4',
    convert: '/media/videos/videos_video/user_1/object_1/m001.mp4',
    like: 0,
    read: 100,
    comment_count: 0,
    publish: true,
    created: '2023-01-01T00:00:00Z',
    updated: '2023-01-01T00:00:00Z',
    author: {
      id: 4,
      nickname: 'ケイマ',
      image: '/media/users/images_user/user_4/MyUs_Profile_04.jpg',
    },
    model_name: 'video',
  },
  {
    id: 5,
    title: '動画テスト5',
    content: '動画テスト5',
    image: '/media/images/images_video/user_1/object_1/005.jpg',
    video: '/media/videos/videos_video/user_1/object_1/m001.mp4',
    convert: '/media/videos/videos_video/user_1/object_1/m001.mp4',
    like: 0,
    read: 100,
    comment_count: 0,
    publish: true,
    created: '2023-01-01T00:00:00Z',
    updated: '2023-01-01T00:00:00Z',
    author: {
      id: 5,
      nickname: 'アン',
      image: '/media/users/images_user/user_5/MyUs_Profile_01.jpg',
    },
    model_name: 'video',
  },
]

const HomePage: NextPage = () => {
  return (
    <>
      <HomeList query={query} datas={datas} videos={datas} />
      {/* <Script src="https://vjs.zencdn.net/7.19.2/video.min.js"></Script>
      <Script src='/pages/api/video_auto.js'></Script>
      <script>$(function() { $('audio').audioPlayer() })</cript> */}
    </>
  )
}
export default HomePage
