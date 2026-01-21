import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { MypageOut } from 'types/internal/user'
import { getSettingMypage } from 'api/internal/setting'
import ErrorCheck from 'components/widgets/Error/Check'
import SettingMyPage from 'components/templates/setting/mypage'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const ret = await getSettingMypage(req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const mypage = ret.value
  return { props: { mypage, ...translations } }
}

interface Props {
  status: number
  mypage: MypageOut
}

export default function SettingMypagePage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <SettingMyPage {...props} />
    </ErrorCheck>
  )
}
