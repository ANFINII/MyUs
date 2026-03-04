import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { UserPage } from 'types/internal/userpage'
import { getUserPage } from 'api/internal/user'
import ErrorCheck from 'components/widgets/Error/Check'
import Userpage from 'components/templates/userpage'

export const getServerSideProps: GetServerSideProps = async ({ locale, req, query }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ulid = String(query.ulid)
  const ret = await getUserPage(ulid, req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const userPage = ret.value
  return { props: { ...translations, ulid, userPage } }
}

interface Props {
  status: number
  ulid: string
  userPage: UserPage
}

export default function UserpagePage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Userpage {...props} />
    </ErrorCheck>
  )
}
