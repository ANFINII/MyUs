import { useQuery } from '@tanstack/react-query'
import { pictureListQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Pictures from 'components/templates/media/picture/list'

export default function PicturesPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }

  const data = useQuery(pictureListQuery(params))
  const queries = { data }

  return (
    <QueryCheck title="Picture" queries={queries}>
      {(props) => <Pictures {...props} page={page} />}
    </QueryCheck>
  )
}
