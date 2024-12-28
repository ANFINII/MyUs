import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Todo } from 'types/internal/media'
import { getTodos } from 'api/internal/media/list'
import Todos from 'components/templates/media/todo/list'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const datas = await getTodos(undefined, req)
  return { props: { datas, ...translations } }
}

interface Props {
  datas: Todo[]
}

export default function TodosPage(props: Props) {
  return <Todos {...props} />
}
