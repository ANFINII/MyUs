import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import ResetConfirm from 'components/templates/account/reset/confirm'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function ResetConfirmPage(): React.JSX.Element {
  return <ResetConfirm />
}
