import { GetStaticProps } from 'next'
import { useRouter } from 'next/router'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getFollower } from 'api/internal/user'
import { searchParams } from 'utils/functions/common'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Followers from 'components/templates/menu/follower'

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function FollowersPage(): React.JSX.Element {
  const router = useRouter()
  const params = searchParams(router.query)

  const query = useQuery({ queryKey: queryKeys.followers(params), queryFn: () => toQuery(getFollower(params)), enabled: router.isReady, placeholderData: keepPreviousData })

  return (
    <QueryCheck queries={{ datas: query }} title="Follower">
      {(props) => <Followers {...props} />}
    </QueryCheck>
  )
}
