// import { GetServerSideProps } from 'next'
import { UserProfile } from 'types/internal/auth'
import SettingProfile from 'components/templates/setting/profile'

// export const getServerSideProps: GetServerSideProps = async (context) => {
//  const cookie = context.req?.headers.cookie
//  const res = await axios.get('/api/profile', {
//   headers: { cookie: cookie! }
//  })
//  const data: ProfileResponse = res.data
//  return {
//   props: { user: data }
//  }
// }

const user: UserProfile = {
  id: 1,
  avatar: '/media/users/images_user/user_5/MyUs_Profile_01.jpg',
  email: 'anfinii56@gmail.com',
  username: 'anfinii56',
  nickname: 'アン',
  fullname: '翁 安',
  lastname: '翁',
  firstname: '安',
  isActive: true,
  isStaff: true,
  lastLogin: 'string',
  dateJoined: 'string',
  year: 1987,
  month: 5,
  day: 6,
  age: 35,
  gender: '男性',
  phone: '090-9678-8552',
  countryCode: 'JP',
  postalCode: '210-0844',
  prefecture: '神奈川県',
  city: '川崎市川崎区渡田新町',
  address: '1-10-8-1',
  building: 'MyUsビル 56F',
  introduction: 'MyUs開発者、ユーザー用',
}

export default function ProfilePage() {
  return <SettingProfile user={user} />
}
