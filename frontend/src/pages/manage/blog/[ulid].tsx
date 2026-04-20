import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Channel } from 'types/internal/channel'
import { Blog } from 'types/internal/media/output'
import { getChannels } from 'api/internal/channel'
import { getManageBlog } from 'api/internal/manage/get'
import ErrorCheck from 'components/widgets/Error/Check'
import ManageBlogEdit from 'components/templates/manage/blog/edit'

export const getServerSideProps: GetServerSideProps = async ({ locale, params, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ulid = String(params?.ulid ?? '')
  const [blogRet, channelsRet] = await Promise.all([getManageBlog(ulid, req), getChannels(req)])
  if (blogRet.isErr()) return { props: { status: blogRet.error.status } }
  if (channelsRet.isErr()) return { props: { status: channelsRet.error.status } }
  const data = blogRet.value
  const channels = channelsRet.value
  return { props: { ...translations, data, channels } }
}

interface Props {
  status: number
  data: Blog
  channels: Channel[]
}

export default function ManageBlogEditPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManageBlogEdit {...props} />
    </ErrorCheck>
  )
}
