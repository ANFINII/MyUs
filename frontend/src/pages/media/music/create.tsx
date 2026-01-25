import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Channel } from 'types/internal/channle'
import { getChannels } from 'api/internal/channel'
import ErrorCheck from 'components/widgets/Error/Check'
import MusicCreate from 'components/templates/media/music/create'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const ret = await getChannels(req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const channels = ret.value
  return { props: { ...translations, channels } }
}

interface Props {
  status: number
  channels: Channel[]
}

export default function MusicCreatePage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <MusicCreate {...props} />
    </ErrorCheck>
  )
}
