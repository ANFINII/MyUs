import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getTodos } from 'api/media'
import { ToDo } from 'types/internal/media'
import Todos from 'components/templates/media/todo/list'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const datas = getTodos()
  return { props: { datas, ...translations } }
}

interface Props {
  datas: ToDo[]
}

export default function TodosPage(props: Props) {
  return <Todos {...props} />
}
