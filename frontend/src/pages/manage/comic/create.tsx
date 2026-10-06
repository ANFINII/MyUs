import { GetStaticProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ComicCreate from 'components/templates/manage/comic/create'

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function ComicCreatePage(): React.JSX.Element {
  const channelsQuery = useQuery({
    queryKey: queryKeys.channels,
    queryFn: () => toQuery(getChannels()),
  })

  const categoriesQuery = useQuery({
    queryKey: queryKeys.categories,
    queryFn: () => toQuery(getCategories()),
  })

  const data = channelsQuery.data && categoriesQuery.data && { channels: channelsQuery.data, categories: categoriesQuery.data }

  return (
    <QueryCheck queries={[channelsQuery, categoriesQuery]} data={data} title="Comic">
      {(props) => <ComicCreate {...props} />}
    </QueryCheck>
  )
}
