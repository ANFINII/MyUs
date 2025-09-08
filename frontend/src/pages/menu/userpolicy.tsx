import { GetStaticProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import UserPolicy from 'components/templates/menu/userpolicy'

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  return { props: translations }
}

export default function UserPolicyPage(): React.JSX.Element {
  return <UserPolicy />
}
