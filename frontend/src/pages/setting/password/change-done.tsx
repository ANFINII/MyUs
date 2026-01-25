import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getUser } from 'api/internal/user'
import ErrorCheck from 'components/widgets/Error/Check'
import PasswordChangeDone from 'components/templates/setting/password/change-done'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ret = await getUser(req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  return { props: { ...translations } }
}

interface Props {
  status: number
}

export default function PasswordChangeDonePage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <PasswordChangeDone />
    </ErrorCheck>
  )
}
