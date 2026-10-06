import { GetStaticPaths, GetStaticProps } from 'next'
import { useRouter } from 'next/router'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import { getManageChat } from 'api/internal/manage/get'
import { useFreshData } from 'components/hooks/useFreshData'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageChatEdit from 'components/templates/manage/chat/edit'

export const getStaticPaths: GetStaticPaths = async () => {
  return { paths: [], fallback: 'blocking' }
}

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function ManageChatEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const channelsQuery = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()) })
  const categoriesQuery = useQuery({ queryKey: queryKeys.categories, queryFn: () => toQuery(getCategories()) })
  const query = useQuery({ queryKey: queryKeys.manageChatDetail(ulid), queryFn: () => toQuery(getManageChat(ulid)), enabled: router.isReady })
  const data = useFreshData({ data: query, channels: channelsQuery, categories: categoriesQuery })

  return (
    <QueryCheck queries={[query, channelsQuery, categoriesQuery]} data={data} title="Chat">
      {(props) => <ManageChatEdit {...props} />}
    </QueryCheck>
  )
}
