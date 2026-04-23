import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Channel } from 'types/internal/channel'
import { Blog } from 'types/internal/media/output'
import { getChannels } from 'api/internal/channel'
import { getManageBlogs } from 'api/internal/manage/get'
import { pageParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Error/Check'
import ManageBlogs from 'components/templates/manage/blog'

export const getServerSideProps: GetServerSideProps = async ({ locale, query, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const { search, page, limit, offset } = pageParams(query)
  const channelsRet = await getChannels(req)
  if (channelsRet.isErr()) return { props: { status: channelsRet.error.status } }
  const channels = channelsRet.value

  const channel = query.channel?.toString() || channels[0]?.ulid || ''
  const blogsRet = await getManageBlogs({ search, channel, limit, offset }, req)
  if (blogsRet.isErr()) return { props: { status: blogsRet.error.status } }
  const { datas, total } = blogsRet.value
  return { props: { ...translations, datas, total, page, channels } }
}

interface Props {
  status: number
  datas: Blog[]
  total: number
  page: number
  channels: Channel[]
}

export default function ManageBlogsPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManageBlogs {...props} />
    </ErrorCheck>
  )
}
