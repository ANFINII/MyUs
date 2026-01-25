import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Follow } from 'types/internal/user'
import { getFollower } from 'api/internal/user'
import { searchParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Error/Check'
import Followers from 'components/templates/menu/follower'

export const getServerSideProps: GetServerSideProps = async ({ locale, query, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const params = searchParams(query)
  const ret = await getFollower(params, req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const datas = ret.value
  return { props: { ...translations, datas } }
}

interface Props {
  status: number
  datas: Follow[]
}

export default function FollowersPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Followers {...props} />
    </ErrorCheck>
  )
}
