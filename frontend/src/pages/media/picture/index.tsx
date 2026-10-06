import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getPictures } from 'api/internal/media/list'
import { pageParams } from 'utils/functions/common'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Pictures from 'components/templates/media/picture/list'

export default function PicturesPage(): React.JSX.Element {
  const router = useAppRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }

  const list = useQuery({ queryKey: queryKeys.mediaPictureList(params), queryFn: () => toQuery(getPictures(params)), enabled: router.isReady, placeholderData: keepPreviousData })
  const queries = { list }

  return (
    <QueryCheck title="Picture" queries={queries}>
      {(props) => <Pictures {...props} page={page} />}
    </QueryCheck>
  )
}
