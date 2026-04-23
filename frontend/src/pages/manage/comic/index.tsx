import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Channel } from 'types/internal/channel'
import { Comic } from 'types/internal/media/output'
import { getChannels } from 'api/internal/channel'
import { getManageComics } from 'api/internal/manage/get'
import { pageParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Error/Check'
import ManageComics from 'components/templates/manage/comic'

export const getServerSideProps: GetServerSideProps = async ({ locale, query, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const { search, page, limit, offset } = pageParams(query)
  const channelsRet = await getChannels(req)
  if (channelsRet.isErr()) return { props: { status: channelsRet.error.status } }
  const channels = channelsRet.value

  const channel = query.channel?.toString() || channels[0]!.ulid
  const comicsRet = await getManageComics({ search, channel, limit, offset }, req)
  if (comicsRet.isErr()) return { props: { status: comicsRet.error.status } }
  const { datas, total } = comicsRet.value
  return { props: { ...translations, datas, total, page, channels } }
}

interface Props {
  status: number
  datas: Comic[]
  total: number
  page: number
  channels: Channel[]
}

export default function ManageComicsPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManageComics {...props} />
    </ErrorCheck>
  )
}
