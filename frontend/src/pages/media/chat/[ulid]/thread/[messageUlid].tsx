import { GetServerSideProps } from 'next'
import { ChatDetailOut } from 'types/internal/media/output'
import { getChat } from 'api/internal/media/detail'
import ErrorCheck from 'components/widgets/Status/Check'
import ChatDetail from 'components/templates/media/chat/detail'

export const getServerSideProps: GetServerSideProps = async ({ req, query }) => {
  const ret = await getChat(String(query.ulid), req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const data = ret.value
  return { props: { data, threadUlid: String(query.messageUlid) } }
}

interface Props {
  status: number
  data: ChatDetailOut
  threadUlid: string
}

export default function ChatThreadPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ChatDetail key={props.data?.detail.ulid} data={props.data} threadUlid={props.threadUlid} />
    </ErrorCheck>
  )
}
