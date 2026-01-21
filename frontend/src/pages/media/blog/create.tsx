import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Channel } from 'types/internal/auth'
import { getChannels } from 'api/internal/user'
import BlogCreate from 'components/templates/media/blog/create'

export const getServerSideProps: GetServerSideProps<Props> = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const ret = await getChannels(req)
  const channels = ret.isOk() ? ret.value : []
  return { props: { ...translations, channels } }
}

interface Props {
  channels: Channel[]
}

export default function BlogCreatePage(props: Props): React.JSX.Element {
  return <BlogCreate {...props} />
}
