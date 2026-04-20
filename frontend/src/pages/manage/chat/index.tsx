import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Channel } from 'types/internal/channel'
import { Chat } from 'types/internal/media/output'
import { getChannels } from 'api/internal/channel'
import { getManageChats } from 'api/internal/manage/get'
import { searchParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Error/Check'
import ManageChats from 'components/templates/manage/chat'

export const getServerSideProps: GetServerSideProps = async ({ locale, query, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const params = searchParams(query)
  const [chatsRet, channelsRet] = await Promise.all([getManageChats(params, req), getChannels(req)])
  if (chatsRet.isErr()) return { props: { status: chatsRet.error.status } }
  if (channelsRet.isErr()) return { props: { status: channelsRet.error.status } }
  const datas = chatsRet.value
  const channels = channelsRet.value
  return { props: { ...translations, datas, channels } }
}

interface Props {
  status: number
  datas: Chat[]
  channels: Channel[]
}

export default function ManageChatsPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManageChats {...props} />
    </ErrorCheck>
  )
}
