import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { MypageOut } from 'types/internal/auth'
import { getSettingMypage } from 'api/internal/setting'
import ErrorCheck from 'components/widgets/ErrorCheck'
import SettingMyPageEdit from 'components/templates/setting/mypage/edit'

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

export default function SettingMypageEditPage(props: Props): JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <SettingMyPageEdit {...props} />
    </ErrorCheck>
  )
}
