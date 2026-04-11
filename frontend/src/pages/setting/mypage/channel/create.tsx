import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import ErrorCheck from 'components/widgets/Error/Check'
import ChannelCreate from 'components/templates/setting/mypage/channel/create'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

interface Props {
  status: number
}

export default function ChannelCreatePage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ChannelCreate />
    </ErrorCheck>
  )
}
