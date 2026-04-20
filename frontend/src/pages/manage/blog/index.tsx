import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Channel } from 'types/internal/channel'
import { Blog } from 'types/internal/media/output'
import { getChannels } from 'api/internal/channel'
import { getManageBlogs } from 'api/internal/manage/get'
import { searchParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Error/Check'
import ManageBlogs from 'components/templates/manage/blog'

export const getServerSideProps: GetServerSideProps = async ({ locale, query, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const params = searchParams(query)
  const [blogsRet, channelsRet] = await Promise.all([getManageBlogs(params, req), getChannels(req)])
  if (blogsRet.isErr()) return { props: { status: blogsRet.error.status } }
  if (channelsRet.isErr()) return { props: { status: channelsRet.error.status } }
  const datas = blogsRet.value
  const channels = channelsRet.value
  return { props: { ...translations, datas, channels } }
}

interface Props {
  status: number
  datas: Blog[]
  channels: Channel[]
}

export default function ManageBlogsPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManageBlogs {...props} />
    </ErrorCheck>
  )
}
