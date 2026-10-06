import { GetStaticPaths, GetStaticProps } from 'next'
import { useRouter } from 'next/router'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import { getManageComic } from 'api/internal/manage/get'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageComicEdit from 'components/templates/manage/comic/edit'

// ビルド時には生成せず、初回アクセス時に外枠（翻訳のみ）を生成する
export const getStaticPaths: GetStaticPaths = async () => {
  return { paths: [], fallback: 'blocking' }
}

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function ManageComicEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const query = useQuery({
    queryKey: queryKeys.manageComicDetail(ulid),
    queryFn: () => toQuery(getManageComic(ulid)),
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

  // フォームの初期値に使うため、キャッシュではなく画面を開いてから取得したデータで表示する
  const data = query.isFetchedAfterMount && query.data && channelsQuery.data && categoriesQuery.data ? { data: query.data, channels: channelsQuery.data, categories: categoriesQuery.data } : undefined

  return (
    <QueryCheck queries={[query, channelsQuery, categoriesQuery]} data={data} title="Comic">
      {(props) => <ManageComicEdit {...props} />}
    </QueryCheck>
  )
}
