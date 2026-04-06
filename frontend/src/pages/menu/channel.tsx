import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Channel } from 'types/internal/channel'
import { getSubscribeChannels } from 'api/internal/channel'
import ErrorCheck from 'components/widgets/Error/Check'
import Channels from 'components/templates/menu/channel'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ret = await getSubscribeChannels(req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const datas = ret.value
  return { props: { ...translations, datas } }
}

interface Props {
  status: number
  datas: Channel[]
}

export default function ChannelsPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Channels {...props} />
    </ErrorCheck>
  )
}
