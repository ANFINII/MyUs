import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import PictureCreate from 'components/templates/manage/picture/create'

export default function PictureCreatePage(): React.JSX.Element {
  const channels = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()) })
  const categories = useQuery({ queryKey: queryKeys.categories, queryFn: () => toQuery(getCategories()) })
  const queries = { channels, categories }

  return (
    <QueryCheck title="Picture" queries={queries} fresh>
      {(props) => <PictureCreate {...props} />}
    </QueryCheck>
  )
}
