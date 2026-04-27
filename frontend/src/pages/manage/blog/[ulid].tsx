import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Category } from 'types/internal/category'
import { Channel } from 'types/internal/channel'
import { Blog } from 'types/internal/media/output'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import { getManageBlog } from 'api/internal/manage/get'
import ErrorCheck from 'components/widgets/Error/Check'
import ManageBlogEdit from 'components/templates/manage/blog/edit'

export const getServerSideProps: GetServerSideProps = async ({ locale, params, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ulid = String(params?.ulid ?? '')
  const [blogRet, channelsRet, categoriesRet] = await Promise.all([getManageBlog(ulid, req), getChannels(req), getCategories(req)])
  if (blogRet.isErr()) return { props: { status: blogRet.error.status } }
  if (channelsRet.isErr()) return { props: { status: channelsRet.error.status } }
  if (categoriesRet.isErr()) return { props: { status: categoriesRet.error.status } }
  const data = blogRet.value
  const channels = channelsRet.value
  const categories = categoriesRet.value
  return { props: { ...translations, data, channels, categories } }
}

interface Props {
  status: number
  data: Blog
  channels: Channel[]
  categories: Category[]
}

export default function ManageBlogEditPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManageBlogEdit {...props} />
    </ErrorCheck>
  )
}
