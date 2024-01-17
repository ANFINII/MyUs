import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getAuth } from 'api/auth'
import TodoCreate from 'components/templates/media/todo/create'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const isAuth = await getAuth(req)
  return { props: { isAuth, ...translations } }
}

interface Props {
  isAuth: boolean
}

export default function TodoCreatePage(props: Props) {
  return <TodoCreate {...props} />
}
