import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { MypageOut } from 'types/internal/auth'
import { getSettingMypage } from 'api/internal/setting'
import SettingMyPageEdit from 'components/templates/setting/mypage/edit'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const mypage = await getSettingMypage(req)
  return { props: { mypage, ...translations } }
}

interface Props {
  mypage: MypageOut
}

export default function SettingMypageEditPage(props: Props): JSX.Element {
  return <SettingMyPageEdit {...props} />
}
