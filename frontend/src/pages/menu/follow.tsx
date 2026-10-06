import { GetStaticProps } from 'next'
import { useRouter } from 'next/router'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getFollow } from 'api/internal/user'
import { searchParams } from 'utils/functions/common'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Follows from 'components/templates/menu/follow'

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function FollowsPage(): React.JSX.Element {
  const router = useRouter()
  const params = searchParams(router.query)

  const query = useQuery({ queryKey: queryKeys.follows(params), queryFn: () => toQuery(getFollow(params)), enabled: router.isReady, placeholderData: keepPreviousData })
  const queries = { datas: query }

  return (
    <QueryCheck queries={queries} title="Follow">
      {(props) => <Follows {...props} />}
    </QueryCheck>
  )
}
