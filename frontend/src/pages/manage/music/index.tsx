import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Channel } from 'types/internal/channel'
import { Music } from 'types/internal/media/output'
import { getChannels } from 'api/internal/channel'
import { getManageMusics } from 'api/internal/manage/music'
import { searchParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Error/Check'
import ManageMusics from 'components/templates/manage/music'

export const getServerSideProps: GetServerSideProps = async ({ locale, query, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const params = searchParams(query)
  const [musicsRet, channelsRet] = await Promise.all([getManageMusics(params, req), getChannels(req)])
  if (musicsRet.isErr()) return { props: { status: musicsRet.error.status } }
  if (channelsRet.isErr()) return { props: { status: channelsRet.error.status } }
  const datas = musicsRet.value
  const channels = channelsRet.value
  return { props: { ...translations, datas, channels } }
}

interface Props {
  status: number
  datas: Music[]
  channels: Channel[]
}

export default function ManageMusicsPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManageMusics {...props} />
    </ErrorCheck>
  )
}
