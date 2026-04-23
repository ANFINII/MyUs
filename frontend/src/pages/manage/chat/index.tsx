import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Channel } from 'types/internal/channel'
import { Chat } from 'types/internal/media/output'
import { getChannels } from 'api/internal/channel'
import { getManageChats } from 'api/internal/manage/get'
import { pageParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Error/Check'
import ManageChats from 'components/templates/manage/chat'

export const getServerSideProps: GetServerSideProps = async ({ locale, query, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const { search, page, limit, offset } = pageParams(query)
  const channelsRet = await getChannels(req)
  if (channelsRet.isErr()) return { props: { status: channelsRet.error.status } }
  const channels = channelsRet.value

  const channel = query.channel?.toString() || channels[0]!.ulid
  const chatsRet = await getManageChats({ search, channel, limit, offset }, req)
  if (chatsRet.isErr()) return { props: { status: chatsRet.error.status } }
  const { datas, total } = chatsRet.value
  return { props: { ...translations, datas, total, page, channels } }
}

interface Props {
  status: number
  datas: Chat[]
  total: number
  page: number
  channels: Channel[]
}

export default function ManageChatsPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManageChats {...props} />
    </ErrorCheck>
  )
}
