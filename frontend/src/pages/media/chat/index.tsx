import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Chat } from 'types/internal/media'
import { getChats } from 'api/internal/media/list'
import Chats from 'components/templates/media/chat/list'

export const getServerSideProps: GetServerSideProps = async ({ locale, query }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const params = { search: String(query.search) }
  const datas = await getChats(params)
  return { props: { datas, ...translations } }
}

interface Props {
  datas: Chat[]
}

export default function ChatsPage(props: Props): JSX.Element {
  return <Chats {...props} />
}
