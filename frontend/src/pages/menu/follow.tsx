import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Follow } from 'types/internal/auth'
import { getFollow } from 'api/internal/user'
import ErrorCheck from 'components/widgets/ErrorCheck'
import Follows from 'components/templates/menu/follow'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const ret = await getFollow(req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const follows = ret.value
  return { props: { follows, ...translations } }
}

interface Props {
  status: number
  follows: Follow[]
}

export default function FollowsPage(props: Props): JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Follows {...props} />
    </ErrorCheck>
  )
}
