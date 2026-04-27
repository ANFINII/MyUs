import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Category } from 'types/internal/category'
import { Channel } from 'types/internal/channel'
import { Video } from 'types/internal/media/output'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import { getManageVideo } from 'api/internal/manage/get'
import ErrorCheck from 'components/widgets/Error/Check'
import ManageVideoEdit from 'components/templates/manage/video/edit'

export const getServerSideProps: GetServerSideProps = async ({ locale, params, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ulid = String(params?.ulid ?? '')
  const [videoRet, channelsRet, categoriesRet] = await Promise.all([getManageVideo(ulid, req), getChannels(req), getCategories(req)])
  if (videoRet.isErr()) return { props: { status: videoRet.error.status } }
  if (channelsRet.isErr()) return { props: { status: channelsRet.error.status } }
  if (categoriesRet.isErr()) return { props: { status: categoriesRet.error.status } }
  const data = videoRet.value
  const channels = channelsRet.value
  const categories = categoriesRet.value
  return { props: { ...translations, data, channels, categories } }
}

interface Props {
  status: number
  data: Video
  channels: Channel[]
  categories: Category[]
}

export default function ManageVideoEditPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManageVideoEdit {...props} />
    </ErrorCheck>
  )
}
