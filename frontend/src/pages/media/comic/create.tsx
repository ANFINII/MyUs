import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Channel } from 'types/internal/auth'
import { getChannels } from 'api/internal/user'
import ComicCreate from 'components/templates/media/comic/create'

export const getServerSideProps: GetServerSideProps<Props> = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const ret = await getChannels(req)
  const channels = ret.isOk() ? ret.value : []
  return { props: { ...translations, channels } }
}

interface Props {
  channels: Channel[]
}

export default function ComicCreatePage(props: Props): React.JSX.Element {
  return <ComicCreate {...props} />
}
