import {GetServerSideProps} from 'next'
import {MypageResponse} from 'types/media'
import Mypage from 'components/templates/Setting/Mypage'

// export const getServerSideProps: GetServerSideProps = async (context) => {
//   const cookie = context.req?.headers.cookie
//   const res = await axios.get('/api/mypage', {
//     headers: { cookie: cookie! }
//   })
//   const data: MypageResponse = res.data
//   return {
//     props: { mypage: data }
//   }
// }

const mypage: MypageResponse = {
  banner: '/media/users/images_mypage/user_5/MyUs_banner.png',
  nickname: 'アン',
  email: 'abc@gmail.com',
  content: 'MyUs開発者です。',
  follower_count: 0,
  following_count: 1,
  plan: 'Free',
  plan_date: '2023-12-31T15:00:00Z',
  is_advertise: true,
}

export default function MyPagePage() {
  return <Mypage mypage={mypage} />
}
