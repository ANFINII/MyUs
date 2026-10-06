import { GetStaticPaths, GetStaticProps } from 'next'
import { useRouter } from 'next/router'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import { getManagePicture } from 'api/internal/manage/get'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManagePictureEdit from 'components/templates/manage/picture/edit'

export const getStaticPaths: GetStaticPaths = async () => {
  return { paths: [], fallback: 'blocking' }
}

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function ManagePictureEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const query = useQuery({
    queryKey: queryKeys.managePictureDetail(ulid),
    queryFn: () => toQuery(getManagePicture(ulid)),
    enabled: router.isReady,
  })

  const channelsQuery = useQuery({
    queryKey: queryKeys.channels,
    queryFn: () => toQuery(getChannels()),
  })

  const categoriesQuery = useQuery({
    queryKey: queryKeys.categories,
    queryFn: () => toQuery(getCategories()),
  })

  const data = query.isFetchedAfterMount && query.data && channelsQuery.data && categoriesQuery.data ? { data: query.data, channels: channelsQuery.data, categories: categoriesQuery.data } : undefined

  return (
    <QueryCheck queries={[query, channelsQuery, categoriesQuery]} data={data} title="Picture">
      {(props) => <ManagePictureEdit {...props} />}
    </QueryCheck>
  )
}
