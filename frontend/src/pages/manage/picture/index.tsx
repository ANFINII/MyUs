import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Channel } from 'types/internal/channel'
import { Picture } from 'types/internal/media/output'
import { getChannels } from 'api/internal/channel'
import { getManagePictures } from 'api/internal/manage/get'
import { pageParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Error/Check'
import ManagePictures from 'components/templates/manage/picture'

export const getServerSideProps: GetServerSideProps = async ({ locale, query, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const { search, page, limit, offset } = pageParams(query)
  const channelsRet = await getChannels(req)
  if (channelsRet.isErr()) return { props: { status: channelsRet.error.status } }
  const channels = channelsRet.value

  const channel = query.channel?.toString() || channels[0]?.ulid || ''
  const picturesRet = await getManagePictures({ search, channel, limit, offset }, req)
  if (picturesRet.isErr()) return { props: { status: picturesRet.error.status } }
  const { datas, total } = picturesRet.value
  return { props: { ...translations, datas, total, page, channels } }
}

interface Props {
  status: number
  datas: Picture[]
  total: number
  page: number
  channels: Channel[]
}

export default function ManagePicturesPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManagePictures {...props} />
    </ErrorCheck>
  )
}
