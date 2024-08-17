import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getServerMypage } from 'api/internal/user'
import { MypageOut } from 'types/internal/auth'
import SettingMyPage from 'components/templates/setting/mypage'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const mypage = await getServerMypage(req)
  return { props: { mypage, ...translations } }
}

interface Props {
  mypage: MypageOut
}

export default function SettingMypagePage(props: Props) {
  return <SettingMyPage {...props} />
}
