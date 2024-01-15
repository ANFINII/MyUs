import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getMypage } from 'api/user'
import { Mypage } from 'types/internal/auth'
import SettingMypageUpdate from 'components/templates/setting/mypage/Update'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const mypage = await getMypage(req)
  return { props: { mypage, ...translations } }
}

interface Props {
  mypage: Mypage
}

export default function SettingMypageUpdatePage(props: Props) {
  return <SettingMypageUpdate {...props} />
}
