import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Channel } from 'types/internal/auth'
import { getChannels } from 'api/internal/user'
import PictureCreate from 'components/templates/media/picture/create'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const ret = await getChannels(req)
  const channels = ret.isOk() ? ret.value : []
  return { props: { ...translations, channels } }
}

interface Props {
  channels: Channel[]
}

export default function PictureCreatePage(props: Props): React.JSX.Element {
  return <PictureCreate {...props} />
}
