import { GetStaticProps } from 'next'
import { useRouter } from 'next/router'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getManageAdvertises } from 'api/internal/manage/get'
import { pageParams } from 'utils/functions/common'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageAdvertises from 'components/templates/manage/advertise'

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function ManageAdvertisesPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }

  const query = useQuery({
    queryKey: queryKeys.manageAdvertiseList(params),
    queryFn: () => toQuery(getManageAdvertises(params)),
    enabled: router.isReady,
    placeholderData: keepPreviousData,
  })

  return (
    <QueryCheck queries={[query]} data={query.data} title="Advertise">
      {(data) => <ManageAdvertises {...data} page={page} />}
    </QueryCheck>
  )
}
