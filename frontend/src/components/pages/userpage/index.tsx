import { useQuery, useSuspenseQuery } from '@tanstack/react-query'
import { userPageAdvertisesQuery, userPageMediaQuery, userPageQuery } from 'lib/query/options'
import { UserPageMedia } from 'types/internal/userpage'
import { selectChannelUlid } from 'utils/functions/channel'
import { searchParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import Userpage from './view'

const initMedia: UserPageMedia = { videos: [], musics: [], blogs: [], comics: [], pictures: [], chats: [] }

export default function UserpagePage(): React.JSX.Element {
  const router = useRouter()
  const params = searchParams(router.query)
  const ulid = String(router.query.ulid ?? '')
  const queryChannel = String(router.query.channel ?? '')
  const { data: userPage } = useSuspenseQuery(userPageQuery(ulid))
  const channelUlid = selectChannelUlid(userPage.channels, queryChannel)
  const media = useQuery({ ...userPageMediaQuery(ulid, channelUlid, params), enabled: channelUlid !== '' })
  const advertises = useQuery(userPageAdvertisesQuery(ulid, params))

  return (
    <Userpage key={`${ulid}${params.search ?? ''}`} userPage={userPage} ulid={ulid} channelUlid={channelUlid} media={media.data ?? initMedia} advertises={advertises.data?.items ?? []} />
  )
}
