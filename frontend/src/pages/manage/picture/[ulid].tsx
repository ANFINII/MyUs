import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import { getManagePicture } from 'api/internal/manage/get'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManagePictureEdit from 'components/templates/manage/picture/edit'

export default function ManagePictureEditPage(): React.JSX.Element {
  const router = useAppRouter()
  const ulid = String(router.query.ulid ?? '')

  const channels = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()) })
  const categories = useQuery({ queryKey: queryKeys.categories, queryFn: () => toQuery(getCategories()) })
  const data = useQuery({ queryKey: queryKeys.managePictureDetail(ulid), queryFn: () => toQuery(getManagePicture(ulid)), enabled: router.isReady })
  const queries = { data, channels, categories }

  return (
    <QueryCheck title="Picture" queries={queries} fresh>
      {(props) => <ManagePictureEdit {...props} />}
    </QueryCheck>
  )
}
