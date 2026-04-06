import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { ChatDetailOut } from 'types/internal/media/detail'
import { getChat } from 'api/internal/media/detail'
import ErrorCheck from 'components/widgets/Error/Check'
import ChatDetail from 'components/templates/media/chat/detail'

export const getServerSideProps: GetServerSideProps = async ({ locale, req, query }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ret = await getChat(String(query.ulid), req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const data = ret.value
  return { props: { ...translations, data, threadUlid: String(query.messageUlid) } }
}

interface Props {
  status: number
  data: ChatDetailOut
  threadUlid: string
}

export default function ChatThreadPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ChatDetail data={props.data} threadUlid={props.threadUlid} />
    </ErrorCheck>
  )
}
