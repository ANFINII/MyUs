import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Channel } from 'types/internal/channel'
import { MypageOut } from 'types/internal/user'
import { getChannels } from 'api/internal/channel'
import { getSettingMypage } from 'api/internal/setting'
import ErrorCheck from 'components/widgets/Error/Check'
import SettingMyPage from 'components/templates/setting/mypage'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ret = await getSettingMypage(req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const mypage = ret.value
  const channelsRet = await getChannels(req)
  const channels = channelsRet.isOk() ? channelsRet.value : []
  return { props: { ...translations, mypage, channels } }
}

interface Props {
  status: number
  mypage: MypageOut
  channels: Channel[]
}

export default function SettingMypagePage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <SettingMyPage {...props} />
    </ErrorCheck>
  )
}
