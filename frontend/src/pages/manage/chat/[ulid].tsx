import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Category } from 'types/internal/category'
import { Channel } from 'types/internal/channel'
import { Chat } from 'types/internal/media/output'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import { getManageChat } from 'api/internal/manage/get'
import ErrorCheck from 'components/widgets/Error/Check'
import ManageChatEdit from 'components/templates/manage/chat/edit'

export const getServerSideProps: GetServerSideProps = async ({ locale, params, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ulid = String(params?.ulid ?? '')
  const [chatRet, channelsRet, categoriesRet] = await Promise.all([getManageChat(ulid, req), getChannels(req), getCategories(req)])
  if (chatRet.isErr()) return { props: { status: chatRet.error.status } }
  if (channelsRet.isErr()) return { props: { status: channelsRet.error.status } }
  if (categoriesRet.isErr()) return { props: { status: categoriesRet.error.status } }
  const data = chatRet.value
  const channels = channelsRet.value
  const categories = categoriesRet.value
  return { props: { ...translations, data, channels, categories } }
}

interface Props {
  status: number
  data: Chat
  channels: Channel[]
  categories: Category[]
}

export default function ManageChatEditPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManageChatEdit {...props} />
    </ErrorCheck>
  )
}
