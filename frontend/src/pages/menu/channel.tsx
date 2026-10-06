import { GetStaticProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getSubscribeChannels } from 'api/internal/channel'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Channels from 'components/templates/menu/channel'

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function ChannelsPage(): React.JSX.Element {
  const query = useQuery({ queryKey: queryKeys.subscribeChannels, queryFn: () => toQuery(getSubscribeChannels()) })
  const queries = { datas: query }

  return (
    <QueryCheck title="Channel" queries={queries}>
      {(props) => <Channels {...props} />}
    </QueryCheck>
  )
}
