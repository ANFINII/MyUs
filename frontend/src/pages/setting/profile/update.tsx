import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { api } from 'lib/axios'
import { Profile } from 'types/internal/auth'
import ProfileUpdate from 'components/templates/setting/profile/Update'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const url = '/profile'
  const user = await api.get(url).then((res) => {
    if (res.status !== 200) throw Error
    return res.data
  })

  // const user: Profile = {
  //   id: 1,
  //   avatar: '/media/users/images_user/user_5/MyUs_Profile_01.jpg',
  //   email: 'anfinii56@gmail.com',
  //   username: 'anfinii56',
  //   nickname: 'アン',
  //   fullname: '翁 安',
  //   lastname: '翁',
  //   firstname: '安',
  //   year: 1987,
  //   month: 5,
  //   day: 6,
  //   age: 35,
  //   gender: '男性',
  //   phone: '090-9678-8552',
  //   countryCode: 'JP',
  //   postalCode: '210-0844',
  //   prefecture: '神奈川県',
  //   city: '川崎市川崎区渡田新町',
  //   address: '1-10-8-1',
  //   building: 'MyUsビル 56F',
  //   introduction: 'MyUs開発者、ユーザー用',
  // }
  return { props: { user, ...translations } }
}

interface Props {
  user: Profile
}

export default function ProfileUpdatePage(props: Props) {
  const { user } = props
  return <ProfileUpdate user={user} />
}
