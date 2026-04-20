import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Channel } from 'types/internal/channel'
import { Picture } from 'types/internal/media/output'
import { getChannels } from 'api/internal/channel'
import { getManagePictures } from 'api/internal/manage/get'
import { searchParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Error/Check'
import ManagePictures from 'components/templates/manage/picture'

export const getServerSideProps: GetServerSideProps = async ({ locale, query, req }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const params = searchParams(query)
  const [picturesRet, channelsRet] = await Promise.all([getManagePictures(params, req), getChannels(req)])
  if (picturesRet.isErr()) return { props: { status: picturesRet.error.status } }
  if (channelsRet.isErr()) return { props: { status: channelsRet.error.status } }
  const datas = picturesRet.value
  const channels = channelsRet.value
  return { props: { ...translations, datas, channels } }
}

interface Props {
  status: number
  datas: Picture[]
  channels: Channel[]
}

export default function ManagePicturesPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ManagePictures {...props} />
    </ErrorCheck>
  )
}
