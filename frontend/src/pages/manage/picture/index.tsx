import { useQuery } from '@tanstack/react-query'
import { channelsQuery, managePictureListQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManagePictures from 'components/templates/manage/picture'

export default function ManagePicturesPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)

  const channels = useQuery(channelsQuery())
  const channel = router.query.channel?.toString() || channels.data?.[0]?.ulid
  const params = { search, channel, limit, offset }

  const data = useQuery({ ...managePictureListQuery(params), enabled: channels.isSuccess })
  const queries = { channels, data }

  return (
    <QueryCheck title="Picture" queries={queries}>
      {(props) => <ManagePictures {...props} page={page} />}
    </QueryCheck>
  )
}
