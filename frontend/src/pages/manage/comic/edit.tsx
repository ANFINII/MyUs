import { useQuery } from '@tanstack/react-query'
import { useParams } from '@tanstack/react-router'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import { getManageComic } from 'api/internal/manage/get'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageComicEdit from 'components/templates/manage/comic/edit'

export default function ManageComicEditPage(): React.JSX.Element {
  const { ulid } = useParams({ from: '/manage/comic/$ulid' })

  const channels = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()) })
  const categories = useQuery({ queryKey: queryKeys.categories, queryFn: () => toQuery(getCategories()) })
  const data = useQuery({ queryKey: queryKeys.manageComicDetail(ulid), queryFn: () => toQuery(getManageComic(ulid)) })
  const queries = { data, channels, categories }

  return (
    <QueryCheck title="Comic" queries={queries} fresh>
      {(props) => <ManageComicEdit {...props} />}
    </QueryCheck>
  )
}
