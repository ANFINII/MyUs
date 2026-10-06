import { GetStaticPaths, GetStaticProps } from 'next'
import { useRouter } from 'next/router'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import { getManageMusic } from 'api/internal/manage/get'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageMusicEdit from 'components/templates/manage/music/edit'

export const getStaticPaths: GetStaticPaths = async () => {
  return { paths: [], fallback: 'blocking' }
}

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function ManageMusicEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const channelsQuery = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()) })
  const categoriesQuery = useQuery({ queryKey: queryKeys.categories, queryFn: () => toQuery(getCategories()) })
  const query = useQuery({ queryKey: queryKeys.manageMusicDetail(ulid), queryFn: () => toQuery(getManageMusic(ulid)), enabled: router.isReady })
  const queries = { data: query, channels: channelsQuery, categories: categoriesQuery }

  return (
    <QueryCheck queries={queries} fresh title="Music">
      {(props) => <ManageMusicEdit {...props} />}
    </QueryCheck>
  )
}
