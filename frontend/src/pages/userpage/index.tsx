import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { userPageAdvertisesQuery, userPageMediaQuery, userPageQuery } from 'lib/query/options'
import { UserPageMedia } from 'types/internal/userpage'
import { selectChannelUlid } from 'utils/functions/channel'
import { searchParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Userpage from 'components/templates/userpage'

const initMedia: UserPageMedia = { videos: [], musics: [], blogs: [], comics: [], pictures: [], chats: [] }

export default function UserpagePage(): React.JSX.Element {
  const { t } = useTranslation()
  const router = useRouter()
  const params = searchParams(router.query)
  const ulid = String(router.query.ulid ?? '')
  const queryChannel = String(router.query.channel ?? '')

  const userPage = useQuery(userPageQuery(ulid))
  const channelUlid = selectChannelUlid(userPage.data?.channels ?? [], queryChannel)
  const media = useQuery({ ...userPageMediaQuery(ulid, channelUlid, params), enabled: channelUlid !== '' })
  const advertises = useQuery(userPageAdvertisesQuery(ulid, params))
  const queries = { userPage }

  return (
    <QueryCheck title={t('media.userpage.title')} queries={queries}>
      {(props) => (
        <Userpage key={params.search ?? ''} {...props} ulid={ulid} channelUlid={channelUlid} media={media.data ?? initMedia} advertises={advertises.data?.items ?? []} />
      )}
    </QueryCheck>
  )
}
