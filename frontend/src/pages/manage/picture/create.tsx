import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Category } from 'types/internal/category'
import { Channel } from 'types/internal/channel'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import ErrorCheck from 'components/widgets/Error/Check'
import PictureCreate from 'components/templates/manage/picture/create'

export const getServerSideProps: GetServerSideProps = async ({ locale, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const [channelRet, categoryRet] = await Promise.all([getChannels(req), getCategories(req)])
  if (channelRet.isErr()) return { props: { status: channelRet.error.status } }
  if (categoryRet.isErr()) return { props: { status: categoryRet.error.status } }
  const channels = channelRet.value
  const categories = categoryRet.value
  return { props: { ...translations, channels, categories } }
}

interface Props {
  status: number
  channels: Channel[]
  categories: Category[]
}

export default function PictureCreatePage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <PictureCreate {...props} />
    </ErrorCheck>
  )
}
