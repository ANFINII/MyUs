import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import Signup from 'components/templates/account/signup'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function SignupPage(): React.JSX.Element {
  return <Signup />
}
