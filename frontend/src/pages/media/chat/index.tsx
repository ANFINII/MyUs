import { GetServerSideProps } from 'next'
import { Chat } from 'types/internal/media/output'
import { getChats } from 'api/internal/media/list'
import { pageParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Status/Check'
import Chats from 'components/templates/media/chat/list'

export const getServerSideProps: GetServerSideProps = async ({ query }) => {
  const { search, limit, offset, page } = pageParams(query)
  const ret = await getChats({ search, limit, offset })
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const { datas, total } = ret.value
  return { props: { datas, total, page } }
}

interface Props {
  status: number
  datas: Chat[]
  total: number
  page: number
}

export default function ChatsPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Chats {...props} />
    </ErrorCheck>
  )
}
