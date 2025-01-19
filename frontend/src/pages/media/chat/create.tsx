import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import ChatCreate from 'components/templates/media/chat/create'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  return { props: { ...translations } }
}

export default function ChatCreatePage(): JSX.Element {
  return <ChatCreate />
}
