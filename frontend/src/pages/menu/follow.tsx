import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Follow } from 'types/internal/auth'
import { getFollow } from 'api/internal/user'
import Follows from 'components/templates/menu/follow'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const follows = await getFollow(req)
  return { props: { follows, ...translations } }
}

interface Props {
  follows: Follow[]
}

export default function FollowsPage(props: Props): JSX.Element {
  return <Follows {...props} />
}
