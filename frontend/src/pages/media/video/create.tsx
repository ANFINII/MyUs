import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Channel } from 'types/internal/channle'
import { getChannels } from 'api/internal/channel'
import VideoCreate from 'components/templates/media/video/create'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const ret = await getChannels(req)
  const channels = ret.isOk() ? ret.value : []
  return { props: { ...translations, channels } }
}

interface Props {
  channels: Channel[]
}

export default function VideoCreatePage(props: Props): React.JSX.Element {
  return <VideoCreate {...props} />
}
