import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Category } from 'types/internal/category'
import { Channel } from 'types/internal/channel'
import { Comic } from 'types/internal/media/output'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import { getManageComic } from 'api/internal/manage/get'
import ErrorCheck from 'components/widgets/Error/Check'
import ManageComicEdit from 'components/templates/manage/comic/edit'

export const getServerSideProps: GetServerSideProps = async ({ locale, params, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ulid = String(params?.ulid ?? '')
  const [comicRet, channelsRet, categoriesRet] = await Promise.all([getManageComic(ulid, req), getChannels(req), getCategories(req)])
  if (comicRet.isErr()) return { props: { status: comicRet.error.status } }
  if (channelsRet.isErr()) return { props: { status: channelsRet.error.status } }
  if (categoriesRet.isErr()) return { props: { status: categoriesRet.error.status } }
  const data = comicRet.value
  const channels = channelsRet.value
  const categories = categoriesRet.value
  return { props: { ...translations, data, channels, categories } }
}

interface Props {
  status: number
  data: Comic
  channels: Channel[]
  categories: Category[]
}

export default function ManageComicEditPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManageComicEdit {...props} />
    </ErrorCheck>
  )
}
