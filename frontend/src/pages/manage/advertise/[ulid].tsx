import { GetStaticPaths, GetStaticProps } from 'next'
import { useRouter } from 'next/router'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getManageAdvertise } from 'api/internal/manage/get'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageAdvertiseEdit from 'components/templates/manage/advertise/edit'

export const getStaticPaths: GetStaticPaths = async () => {
  return { paths: [], fallback: 'blocking' }
}

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function ManageAdvertiseEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const query = useQuery({ queryKey: queryKeys.manageAdvertiseDetail(ulid), queryFn: () => toQuery(getManageAdvertise(ulid)), enabled: router.isReady })
  const queries = { data: query }

  return (
    <QueryCheck title="Advertise" queries={queries} fresh>
      {(props) => <ManageAdvertiseEdit {...props} />}
    </QueryCheck>
  )
}
