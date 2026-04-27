import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Category } from 'types/internal/category'
import { Channel } from 'types/internal/channel'
import { Picture } from 'types/internal/media/output'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import { getManagePicture } from 'api/internal/manage/get'
import ErrorCheck from 'components/widgets/Error/Check'
import ManagePictureEdit from 'components/templates/manage/picture/edit'

export const getServerSideProps: GetServerSideProps = async ({ locale, params, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ulid = String(params?.ulid ?? '')
  const [pictureRet, channelsRet, categoriesRet] = await Promise.all([getManagePicture(ulid, req), getChannels(req), getCategories(req)])
  if (pictureRet.isErr()) return { props: { status: pictureRet.error.status } }
  if (channelsRet.isErr()) return { props: { status: channelsRet.error.status } }
  if (categoriesRet.isErr()) return { props: { status: categoriesRet.error.status } }
  const data = pictureRet.value
  const channels = channelsRet.value
  const categories = categoriesRet.value
  return { props: { ...translations, data, channels, categories } }
}

interface Props {
  status: number
  data: Picture
  channels: Channel[]
  categories: Category[]
}

export default function ManagePictureEditPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManagePictureEdit {...props} />
    </ErrorCheck>
  )
}
