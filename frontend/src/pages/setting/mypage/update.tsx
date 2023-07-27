import { Mypage } from 'types/auth'
import MypageUpdate from 'components/templates/Setting/Mypage/Update'

// export const getServerSideProps: GetServerSideProps = async (context) => {
//   const cookie = context.req?.headers.cookie
//   const res = await axios.get('/api/mypage', {
//     headers: {cookie: cookie!}
//   })
//   const data: MypageResponse = res.data
//   return {
//     props: {mypage: data}
//   }
// }

const mypage: Mypage = {
  id: 1,
  banner: '/media/users/images_mypage/user_5/MyUs_banner.png',
  nickname: 'アン',
  email: 'abc@gmail.com',
  content: 'MyUs開発者です。',
  followerCount: 0,
  followingCount: 1,
  plan: 'Free',
  planDate: '2023-12-31T15:00:00Z',
  isAdvertise: true,
}

export default function MyPageUpdatePage() {
  return <MypageUpdate mypage={mypage} />
}
