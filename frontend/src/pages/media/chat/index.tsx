import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Chat } from 'types/internal/media'
import { getChats } from 'api/internal/media/list'
import { searchParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Error/Check'
import Chats from 'components/templates/media/chat/list'

export const getServerSideProps: GetServerSideProps = async ({ locale, query }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const params = searchParams(query)
  const ret = await getChats(params)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const datas = ret.value
  return { props: { datas, ...translations } }
}

interface Props {
  status: number
  datas: Chat[]
}

export default function ChatsPage(props: Props): JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Chats {...props} />
    </ErrorCheck>
  )
}
