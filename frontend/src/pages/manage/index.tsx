import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { getUser } from 'api/internal/user'
import ErrorCheck from 'components/widgets/Error/Check'
import Manage from 'components/templates/manage'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ret = await getUser(req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  return { props: { ...translations } }
}

interface Props {
  status: number
}

export default function ManagePage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Manage />
    </ErrorCheck>
  )
}
