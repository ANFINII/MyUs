import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Channel } from 'types/internal/channel'
import { Video } from 'types/internal/media/output'
import { getChannels } from 'api/internal/channel'
import { getManageVideo } from 'api/internal/manage/video'
import ErrorCheck from 'components/widgets/Error/Check'
import ManageVideoEdit from 'components/templates/manage/video/edit'

export const getServerSideProps: GetServerSideProps = async ({ locale, params, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ulid = String(params?.ulid ?? '')
  const [videoRet, channelsRet] = await Promise.all([getManageVideo(ulid, req), getChannels(req)])
  if (videoRet.isErr()) return { props: { status: videoRet.error.status } }
  if (channelsRet.isErr()) return { props: { status: channelsRet.error.status } }
  const data = videoRet.value
  const channels = channelsRet.value
  return { props: { ...translations, data, channels } }
}

interface Props {
  status: number
  data: Video
  channels: Channel[]
}

export default function ManageVideoEditPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManageVideoEdit {...props} />
    </ErrorCheck>
  )
}
