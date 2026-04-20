import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Channel } from 'types/internal/channel'
import { Video } from 'types/internal/media/output'
import { getChannels } from 'api/internal/channel'
import { getManageVideos } from 'api/internal/manage/get'
import { searchParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Error/Check'
import ManageVideos from 'components/templates/manage/video'

export const getServerSideProps: GetServerSideProps = async ({ locale, query, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const params = searchParams(query)
  const [videosRet, channelsRet] = await Promise.all([getManageVideos(params, req), getChannels(req)])
  if (videosRet.isErr()) return { props: { status: videosRet.error.status } }
  if (channelsRet.isErr()) return { props: { status: channelsRet.error.status } }
  const datas = videosRet.value
  const channels = channelsRet.value
  return { props: { ...translations, datas, channels } }
}

interface Props {
  status: number
  datas: Video[]
  channels: Channel[]
}

export default function ManageVideosPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManageVideos {...props} />
    </ErrorCheck>
  )
}
