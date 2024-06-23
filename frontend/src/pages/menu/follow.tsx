import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getServerFollow } from 'api/user'
import { Follow } from 'types/internal/auth'
import Follows from 'components/templates/menu/follow'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const follows = await getServerFollow(req)
  return { props: { follows, ...translations } }
}

interface Props {
  follows: Follow[]
}

export default function FollowsPage(props: Props) {
  return <Follows {...props} />
}
