import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getChannels } from 'api/internal/channel'
import { getManagePictures } from 'api/internal/manage/get'
import { pageParams } from 'utils/functions/common'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManagePictures from 'components/templates/manage/picture'

export default function ManagePicturesPage(): React.JSX.Element {
  const router = useAppRouter()
  const { search, page, limit, offset } = pageParams(router.query)

  const channelsQuery = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()), enabled: router.isReady })

  const channels = channelsQuery.data ?? []
  const channel = router.query.channel?.toString() || channels[0]?.ulid
  const params = { search, channel, limit, offset }

  const query = useQuery({
    queryKey: queryKeys.managePictureList(params),
    queryFn: () => toQuery(getManagePictures(params)),
    enabled: channelsQuery.isSuccess,
    placeholderData: keepPreviousData,
  })
  const queries = { channels: channelsQuery, list: query }

  return (
    <QueryCheck title="Picture" queries={queries}>
      {(props) => <ManagePictures {...props} page={page} />}
    </QueryCheck>
  )
}
