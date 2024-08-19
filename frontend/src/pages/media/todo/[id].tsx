import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getServerTodo } from 'api/internal/media/detail'
import { Todo } from 'types/internal/media'
import TodoDetail from 'components/templates/media/todo/detail'

export const getServerSideProps: GetServerSideProps = async ({ locale, req, query }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const data = await getServerTodo(req, Number(query.id))
  return { props: { data, ...translations } }
}

interface Props {
  data: Todo
}

export default function TodoDetailPage(props: Props) {
  return <TodoDetail {...props} />
}
