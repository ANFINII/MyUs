import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import Login from 'components/templates/account/login'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function LoginPage(): React.JSX.Element {
  return <Login />
}
