import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getServerFollower } from 'api/user'
import { Follow } from 'types/internal/auth'
import Followers from 'components/templates/menu/follower'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const follows = await getServerFollower(req)
  return { props: { follows, ...translations } }
}

interface Props {
  follows: Follow[]
}

export default function FollowersPage(props: Props) {
  return <Followers {...props} />
}
