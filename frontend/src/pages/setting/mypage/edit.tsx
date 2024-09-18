import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getServerSettingMypage } from 'api/internal/setting'
import { MypageOut } from 'types/internal/auth'
import SettingMyPageEdit from 'components/templates/setting1/mypage/edit'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const mypage = await getServerSettingMypage(req)
  return { props: { mypage, ...translations } }
}

interface Props {
  mypage: MypageOut
}

export default function SettingMypageEditPage(props: Props) {
  return <SettingMyPageEdit {...props} />
}
