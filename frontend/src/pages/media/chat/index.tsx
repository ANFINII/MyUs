import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getChats } from 'api/media'
import { Chat } from 'types/internal/media'
import Chats from 'components/templates/media/chat/list'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const datas = getChats()
  return { props: { datas, ...translations } }
}

interface Props {
  datas: Chat[]
}

export default function ChatsPage(props: Props) {
  return <Chats {...props} />
}
