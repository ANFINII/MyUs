import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Channel } from 'types/internal/channle'
import { getChannels } from 'api/internal/channel'
import ErrorCheck from 'components/widgets/Error/Check'
import ComicCreate from 'components/templates/media/comic/create'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ret = await getChannels(req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const channels = ret.value
  return { props: { ...translations, channels } }
}

interface Props {
  status: number
  channels: Channel[]
}

export default function ComicCreatePage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ComicCreate {...props} />
    </ErrorCheck>
  )
}
