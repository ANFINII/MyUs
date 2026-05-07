import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { MypageOut } from 'types/internal/user'
import { getSettingMypage } from 'api/internal/setting'
import ErrorCheck from 'components/widgets/Error/Check'
import Payment from 'components/templates/setting/payment'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ret = await getSettingMypage(req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  return { props: { ...translations, mypage: ret.value } }
}

interface Props {
  status: number
  mypage: MypageOut
}

export default function PaymentPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Payment {...props} />
    </ErrorCheck>
  )
}
