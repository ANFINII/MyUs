import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { UserPage, UserPageMedia } from 'types/internal/userpage'
import { getUserPage, getUserPageMedia } from 'api/internal/user'
import ErrorCheck from 'components/widgets/Error/Check'
import Userpage from 'components/templates/userpage'

export const getServerSideProps: GetServerSideProps = async ({ locale, req, query }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ulid = String(query.ulid)
  const ret = await getUserPage(ulid, req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const userPage = ret.value

  const initMedia: UserPageMedia = { videos: [], musics: [], comics: [], pictures: [], blogs: [], chats: [] }
  const queryChannel = typeof query.channel === 'string' ? query.channel : undefined
  const channelUlid = userPage.channels.find((c) => c.ulid === queryChannel || c.isDefault)!.ulid
  const mediaRet = await getUserPageMedia(ulid, channelUlid, req)
  const media = mediaRet.isOk() ? mediaRet.value : initMedia

  return { props: { ...translations, ulid, channelUlid, userPage, media } }
}

interface Props {
  status: number
  ulid: string
  channelUlid: string
  userPage: UserPage
  media: UserPageMedia
}

export default function UserpagePage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Userpage {...props} />
    </ErrorCheck>
  )
}
