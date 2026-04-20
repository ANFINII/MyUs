import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Channel } from 'types/internal/channel'
import { Comic } from 'types/internal/media/output'
import { getChannels } from 'api/internal/channel'
import { getManageComics } from 'api/internal/manage/get'
import { searchParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Error/Check'
import ManageComics from 'components/templates/manage/comic'

export const getServerSideProps: GetServerSideProps = async ({ locale, query, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const params = searchParams(query)
  const [comicsRet, channelsRet] = await Promise.all([getManageComics(params, req), getChannels(req)])
  if (comicsRet.isErr()) return { props: { status: comicsRet.error.status } }
  if (channelsRet.isErr()) return { props: { status: channelsRet.error.status } }
  const datas = comicsRet.value
  const channels = channelsRet.value
  return { props: { ...translations, datas, channels } }
}

interface Props {
  status: number
  datas: Comic[]
  channels: Channel[]
}

export default function ManageComicsPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManageComics {...props} />
    </ErrorCheck>
  )
}
