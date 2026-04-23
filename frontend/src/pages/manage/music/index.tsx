import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Channel } from 'types/internal/channel'
import { Music } from 'types/internal/media/output'
import { getChannels } from 'api/internal/channel'
import { getManageMusics } from 'api/internal/manage/get'
import { pageParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Error/Check'
import ManageMusics from 'components/templates/manage/music'

export const getServerSideProps: GetServerSideProps = async ({ locale, query, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const { search, page, limit, offset } = pageParams(query)
  const channelsRet = await getChannels(req)
  if (channelsRet.isErr()) return { props: { status: channelsRet.error.status } }
  const channels = channelsRet.value

  const channel = query.channel?.toString() || channels[0]?.ulid || ''
  const musicsRet = await getManageMusics({ search, channel, limit, offset }, req)
  if (musicsRet.isErr()) return { props: { status: musicsRet.error.status } }
  const { datas, total } = musicsRet.value
  return { props: { ...translations, datas, total, page, channels } }
}

interface Props {
  status: number
  datas: Music[]
  total: number
  page: number
  channels: Channel[]
}

export default function ManageMusicsPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManageMusics {...props} />
    </ErrorCheck>
  )
}
