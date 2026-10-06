import { GetServerSideProps } from 'next'
import { UserPage, UserPageMedia } from 'types/internal/userpage'
import { getUserPage, getUserPageMedia } from 'api/internal/user'
import ErrorCheck from 'components/widgets/Status/Check'
import Userpage from 'components/templates/userpage'

export const getServerSideProps: GetServerSideProps = async ({ req, query }) => {
  const ulid = String(query.ulid)
  const ret = await getUserPage(ulid, req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const userPage = ret.value

  const initMedia: UserPageMedia = { videos: [], musics: [], blogs: [], comics: [], pictures: [], chats: [] }
  const queryChannel = typeof query.channel === 'string' ? query.channel : undefined
  const channel = userPage.channels.find((c) => c.ulid === queryChannel) || userPage.channels.find((c) => c.isDefault)
  const channelUlid = channel!.ulid
  const mediaRet = await getUserPageMedia(ulid, channelUlid, req)
  const media = mediaRet.isOk() ? mediaRet.value : initMedia

  return { props: { ulid, channelUlid, userPage, media } }
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
