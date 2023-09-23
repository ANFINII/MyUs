import { GetServerSideProps } from 'next'
import { Search, Video } from 'types/media'
import Videos from 'components/templates/media/video/list'

export async function getVideoList() {
  const BASEURL = process.env.NEXT_PUBLIC_API_URL
  const res = await fetch(BASEURL + '/api/video')
  if (res.status !== 200) Error
  return res.json()
}

export const getServerSideProps: GetServerSideProps = async () => {
  const datas = await getVideoList()

  // const datas: Video[] = [
  //   {
  //     id: 1,
  //     title: '動画テスト1',
  //     content: '動画テスト1',
  //     image: '/media/images/images_video/user_1/object_1/001.jpg',
  //     video: '/media/videos/videos_video/user_1/object_1/m001.mp4',
  //     convert: '/media/videos/videos_video/user_1/object_1/m001.mp4',
  //     like: 0,
  //     read: 101,
  //     commentCount: 0,
  //     publish: true,
  //     created: '2023-01-01T00:00:00Z',
  //     updated: '2023-01-01T00:00:00Z',
  //     author: {
  //       id: 1,
  //       nickname: 'アンさん',
  //       image: '/media/users/images_user/user_1/An_Okina.jpg',
  //     },
  //     modelName: 'video',
  //   },
  //   {
  //     id: 2,
  //     title: '動画テスト2',
  //     content: '動画テスト2',
  //     image: '/media/images/images_video/user_1/object_1/002.jpg',
  //     video: '/media/videos/videos_video/user_1/object_1/m001.mp4',
  //     convert: '/media/videos/videos_video/user_1/object_1/m001.mp4',
  //     like: 0,
  //     read: 100,
  //     commentCount: 0,
  //     publish: true,
  //     created: '2023-01-01T00:00:00Z',
  //     updated: '2023-01-01T00:00:00Z',
  //     author: {
  //       id: 2,
  //       nickname: 'ショウエン',
  //       image: '/media/users/images_user/user_2/MyUs_Profile_02.jpg',
  //     },
  //     modelName: 'video',
  //   },
  //   {
  //     id: 3,
  //     title: '動画テスト3',
  //     content: '動画テスト3',
  //     image: '/media/images/images_video/user_1/object_1/003.jpg',
  //     video: '/media/videos/videos_video/user_1/object_1/m001.mp4',
  //     convert: '/media/videos/videos_video/user_1/object_1/m001.mp4',
  //     like: 0,
  //     read: 100,
  //     commentCount: 0,
  //     publish: true,
  //     created: '2023-01-01T00:00:00Z',
  //     updated: '2023-01-01T00:00:00Z',
  //     author: {
  //       id: 3,
  //       nickname: 'ソウヒ',
  //       image: '/media/users/images_user/user_3/MyUs_Profile_03.jpg',
  //     },
  //     modelName: 'video',
  //   },
  //   {
  //     id: 4,
  //     title: '動画テスト4',
  //     content: '動画テスト4',
  //     image: '/media/images/images_video/user_1/object_1/004.jpg',
  //     video: '/media/videos/videos_video/user_1/object_1/m001.mp4',
  //     convert: '/media/videos/videos_video/user_1/object_1/m001.mp4',
  //     like: 0,
  //     read: 100,
  //     commentCount: 0,
  //     publish: true,
  //     created: '2023-01-01T00:00:00Z',
  //     updated: '2023-01-01T00:00:00Z',
  //     author: {
  //       id: 4,
  //       nickname: 'ケイマ',
  //       image: '/media/users/images_user/user_4/MyUs_Profile_04.jpg',
  //     },
  //     modelName: 'video',
  //   },
  //   {
  //     id: 5,
  //     title: '動画テスト5',
  //     content: '動画テスト5',
  //     image: '/media/images/images_video/user_1/object_1/005.jpg',
  //     video: '/media/videos/videos_video/user_1/object_1/m001.mp4',
  //     convert: '/media/videos/videos_video/user_1/object_1/m001.mp4',
  //     like: 0,
  //     read: 100,
  //     commentCount: 0,
  //     publish: true,
  //     created: '2023-01-01T00:00:00Z',
  //     updated: '2023-01-01T00:00:00Z',
  //     author: {
  //       id: 5,
  //       nickname: 'アン',
  //       image: '/media/users/images_user/user_5/MyUs_Profile_01.jpg',
  //     },
  //     modelName: 'video',
  //   },
  // ]
  return {
    props: { datas },
  }
}

const search: Search = {
  name: 'test',
  count: 0,
}

interface Props {
  datas: Video[]
}

export default function VideosPage(props: Props) {
  const { datas } = props
  return <Videos search={search} datas={datas} />
}
