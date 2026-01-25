import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import Reset from 'components/templates/account/reset'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function ResetPage(): React.JSX.Element {
  return <Reset />
}
