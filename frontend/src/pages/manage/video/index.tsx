import { GetStaticProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getChannels } from 'api/internal/channel'
import { getManageVideos } from 'api/internal/manage/get'
import { pageParams } from 'utils/functions/common'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageVideos from 'components/templates/manage/video'

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function ManageVideosPage(): React.JSX.Element {
  const router = useAppRouter()
  const { search, page, limit, offset } = pageParams(router.query)

  const channelsQuery = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()), enabled: router.isReady })

  const channels = channelsQuery.data ?? []
  const channel = router.query.channel?.toString() || channels[0]?.ulid
  const params = { search, channel, limit, offset }

  const query = useQuery({
    queryKey: queryKeys.manageVideoList(params),
    queryFn: () => toQuery(getManageVideos(params)),
    enabled: channelsQuery.isSuccess,
    placeholderData: keepPreviousData,
  })
  const queries = { channels: channelsQuery, list: query }

  return (
    <QueryCheck title="Video" queries={queries}>
      {({ list }) => <ManageVideos {...list} page={page} channels={channels} />}
    </QueryCheck>
  )
}
