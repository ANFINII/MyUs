import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Channel } from 'types/internal/channel'
import { Video } from 'types/internal/media/output'
import { getChannels } from 'api/internal/channel'
import { getManageVideos } from 'api/internal/manage/get'
import { pageParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Error/Check'
import ManageVideos from 'components/templates/manage/video'

export const getServerSideProps: GetServerSideProps = async ({ locale, query, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const { search, page, limit, offset } = pageParams(query)
  const channelsRet = await getChannels(req)
  if (channelsRet.isErr()) return { props: { status: channelsRet.error.status } }
  const channels = channelsRet.value

  const channel = query.channel?.toString() || channels[0]!.ulid
  const videosRet = await getManageVideos({ search, channel, limit, offset }, req)
  if (videosRet.isErr()) return { props: { status: videosRet.error.status } }
  const { datas, total } = videosRet.value
  return { props: { ...translations, datas, total, page, channels } }
}

interface Props {
  status: number
  datas: Video[]
  total: number
  page: number
  channels: Channel[]
}

export default function ManageVideosPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManageVideos {...props} />
    </ErrorCheck>
  )
}
