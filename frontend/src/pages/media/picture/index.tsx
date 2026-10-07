import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { useSearch } from '@tanstack/react-router'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getPictures } from 'api/internal/media/list'
import { pageParams } from 'utils/functions/common'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Pictures from 'components/templates/media/picture/list'

export default function PicturesPage(): React.JSX.Element {
  const query = useSearch({ strict: false })
  const { search, page, limit, offset } = pageParams(query)
  const params = { search, limit, offset }

  const data = useQuery({ queryKey: queryKeys.mediaPictureList(params), queryFn: () => toQuery(getPictures(params)), placeholderData: keepPreviousData })
  const queries = { data }

  return (
    <QueryCheck title="Picture" queries={queries}>
      {(props) => <Pictures {...props} page={page} />}
    </QueryCheck>
  )
}
