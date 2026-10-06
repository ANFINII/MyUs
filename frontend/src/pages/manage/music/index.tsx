import { GetStaticProps } from 'next'
import { useRouter } from 'next/router'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getChannels } from 'api/internal/channel'
import { getManageMusics } from 'api/internal/manage/get'
import { pageParams } from 'utils/functions/common'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageMusics from 'components/templates/manage/music'

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function ManageMusicsPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)

  const channelsQuery = useQuery({
    queryKey: queryKeys.channels,
    queryFn: () => toQuery(getChannels()),
    enabled: router.isReady,
  })

  const channels = channelsQuery.data ?? []
  const channel = router.query.channel?.toString() || channels[0]?.ulid
  const params = { search, channel, limit, offset }

  const query = useQuery({
    queryKey: queryKeys.manageMusicList(params),
    queryFn: () => toQuery(getManageMusics(params)),
    enabled: channelsQuery.isSuccess,
    placeholderData: keepPreviousData,
  })

  return (
    <QueryCheck queries={[channelsQuery, query]} data={query.data} title="Music">
      {(data) => <ManageMusics {...data} page={page} channels={channels} />}
    </QueryCheck>
  )
}
