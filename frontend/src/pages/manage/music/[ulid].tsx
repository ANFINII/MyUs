import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Channel } from 'types/internal/channel'
import { Music } from 'types/internal/media/output'
import { getChannels } from 'api/internal/channel'
import { getManageMusic } from 'api/internal/manage/get'
import ErrorCheck from 'components/widgets/Error/Check'
import ManageMusicEdit from 'components/templates/manage/music/edit'

export const getServerSideProps: GetServerSideProps = async ({ locale, params, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ulid = String(params?.ulid ?? '')
  const [musicRet, channelsRet] = await Promise.all([getManageMusic(ulid, req), getChannels(req)])
  if (musicRet.isErr()) return { props: { status: musicRet.error.status } }
  if (channelsRet.isErr()) return { props: { status: channelsRet.error.status } }
  const data = musicRet.value
  const channels = channelsRet.value
  return { props: { ...translations, data, channels } }
}

interface Props {
  status: number
  data: Music
  channels: Channel[]
}

export default function ManageMusicEditPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManageMusicEdit {...props} />
    </ErrorCheck>
  )
}
