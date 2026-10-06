import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { UserPageMedia } from 'types/internal/userpage'
import { getUserPage, getUserPageMedia } from 'api/internal/user'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Userpage from 'components/templates/userpage'

const initMedia: UserPageMedia = { videos: [], musics: [], blogs: [], comics: [], pictures: [], chats: [] }

export default function UserpagePage(): React.JSX.Element {
  const router = useAppRouter()
  const ulid = String(router.query.ulid ?? '')
  const queryChannel = typeof router.query.channel === 'string' ? router.query.channel : undefined

  const userPage = useQuery({ queryKey: queryKeys.userPage(ulid), queryFn: () => toQuery(getUserPage(ulid)) })

  const channels = userPage.data?.channels ?? []
  const channelUlid = (channels.find((c) => c.ulid === queryChannel) ?? channels.find((c) => c.isDefault))?.ulid ?? ''

  const media = useQuery({
    queryKey: queryKeys.userPageMedia(ulid, channelUlid),
    queryFn: () => toQuery(getUserPageMedia(ulid, channelUlid)),
    enabled: channelUlid !== '',
    placeholderData: keepPreviousData,
  })
  const queries = { userPage }

  return (
    <QueryCheck title="ユーザーページ" queries={queries} fresh>
      {(props) => <Userpage {...props} ulid={ulid} channelUlid={channelUlid} media={media.data ?? initMedia} />}
    </QueryCheck>
  )
}
