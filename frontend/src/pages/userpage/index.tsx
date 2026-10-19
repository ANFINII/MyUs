import { useTranslation } from 'react-i18next'
import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { UserPageMedia } from 'types/internal/userpage'
import { getUserPage, getUserPageAdvertises, getUserPageMedia } from 'api/internal/user'
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

  const userPage = useQuery({ queryKey: queryKeys.userPage(ulid), queryFn: () => toQuery(getUserPage(ulid)) })
  const channels = userPage.data?.channels ?? []
  const channelUlid = (channels.find((c) => c.ulid === queryChannel) ?? channels.find((c) => c.isDefault))?.ulid ?? ''

  const media = useQuery({
    queryKey: queryKeys.userPageMedia(ulid, channelUlid, params),
    queryFn: () => toQuery(getUserPageMedia(ulid, channelUlid, params)),
    enabled: channelUlid !== '',
    placeholderData: keepPreviousData,
  })
  const advertises = useQuery({ queryKey: queryKeys.userPageAdvertise(ulid, params), queryFn: () => toQuery(getUserPageAdvertises(ulid, params)), placeholderData: keepPreviousData })
  const queries = { userPage }

  return (
    <QueryCheck title={t('media.userpage.title')} queries={queries} fresh>
      {(props) => (
        <Userpage key={params.search ?? ''} {...props} ulid={ulid} channelUlid={channelUlid} media={media.data ?? initMedia} advertises={advertises.data?.items ?? []} />
      )}
    </QueryCheck>
  )
}
