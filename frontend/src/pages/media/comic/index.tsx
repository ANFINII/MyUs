import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getComics } from 'api/internal/media/list'
import { pageParams } from 'utils/functions/common'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Comics from 'components/templates/media/comic/list'

export default function ComicsPage(): React.JSX.Element {
  const router = useAppRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }

  const query = useQuery({ queryKey: queryKeys.mediaComicList(params), queryFn: () => toQuery(getComics(params)), enabled: router.isReady, placeholderData: keepPreviousData })
  const queries = { list: query }

  return (
    <QueryCheck title="Comic" queries={queries}>
      {(props) => <Comics {...props} page={page} />}
    </QueryCheck>
  )
}
