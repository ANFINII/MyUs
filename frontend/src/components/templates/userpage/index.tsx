import { ChangeEvent, useState } from 'react'
import { Option } from 'types/internal/other'
import { UserPage, UserPageMedia } from 'types/internal/userpage'
import { getUserPageMedia, postFollow } from 'api/internal/user'
import { useUser } from 'components/hooks/useUser'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import ExImage from 'components/parts/ExImage'
import SelectBox from 'components/parts/Input/SelectBox'
import HStack from 'components/parts/Stack/Horizontal'
import Tabs, { TabItem } from 'components/parts/Tabs'
import FollowButton from 'components/widgets/FollowButton'
import MediaBlog from 'components/widgets/Media/Index/Blog'
import MediaChat from 'components/widgets/Media/Index/Chat'
import MediaComic from 'components/widgets/Media/Index/Comic'
import MediaMusic from 'components/widgets/Media/Index/Music'
import MediaPicture from 'components/widgets/Media/Index/Picture'
import MediaVideo from 'components/widgets/Media/Index/Video'
import MediaIndex from 'components/widgets/Media/List/Index'
import FollowDeleteModal from 'components/widgets/Modal/FollowDelete'
import style from './UserPage.module.scss'

const enum TabKey {
  Info = 'info',
  Posts = 'posts',
}

interface Props {
  ulid: string
  userPage: UserPage
  media: UserPageMedia
}

export default function Userpage(props: Props): React.JSX.Element {
  const { ulid, userPage, media } = props
  const { avatar, banner, nickname, email, content, dateJoined, channels } = userPage

  const { user } = useUser()
  const [isModal, setIsModal] = useState<boolean>(false)
  const [isFollow, setIsFollow] = useState<boolean>(userPage.isFollow)
  const [followerCount, setFollowerCount] = useState<number>(userPage.followerCount)
  const [channelUlid, setChannelUlid] = useState<string>(channels.find((c) => c.isDefault)!.ulid)
  const [selectedTab, setSelectedTab] = useState<TabKey>(TabKey.Info)
  const [newMedia, setNewMedia] = useState<UserPageMedia>(media)

  const isSelf = user.isActive && user.nickname === nickname
  const formattedDate = new Date(dateJoined).toLocaleDateString('ja-JP', { year: 'numeric', month: 'long', day: 'numeric' })
  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))
  const selectedChannel = channels.find((c) => c.ulid === channelUlid)

  const tabItems: TabItem<TabKey>[] = [
    { key: TabKey.Info, label: '情報' },
    { key: TabKey.Posts, label: '投稿' },
  ]

  const handleModal = () => setIsModal(!isModal)

  const handleFollow = async () => {
    if (isFollow && !isModal) {
      handleModal()
      return
    }
    const ret = await postFollow({ ulid, isFollow: !isFollow })
    if (ret.isErr()) return
    setIsFollow(ret.value.isFollow)
    setFollowerCount(ret.value.followerCount)
    if (isModal) handleModal()
  }

  const handleChannelSelect = async (e: ChangeEvent<HTMLSelectElement>) => {
    const selectedlUlid = e.target.value
    if (selectedlUlid === channelUlid) return
    const ret = await getUserPageMedia(ulid, selectedlUlid)
    if (ret.isErr()) return
    setChannelUlid(selectedlUlid)
    setNewMedia(ret.value)
  }

  return (
    <Main metaTitle={`${nickname} - MyUs`}>
      <div className={style.userpage}>
        <figure className={style.banner}>
          <ExImage src={banner} title={nickname} />
        </figure>

        <HStack align="start" justify="between">
          <div className={style.author}>
            <ExImage src={avatar} title={nickname} className={style.avatar} />
            <div className={style.author_info}>
              <span className={style.nickname} title={nickname}>
                {nickname}
              </span>
              <span className={style.follower}>フォロワー数 {followerCount}</span>
              <span className={style.following}>フォロー数 {userPage.followingCount}</span>
            </div>
            <span className={style.follow_button}>
              <FollowButton isFollow={isFollow} disabled={isSelf || !user.isActive} onClick={handleFollow} />
            </span>
          </div>
          <SelectBox label="チャンネル" value={channelUlid} options={channelOptions} className={style.channel} onChange={handleChannelSelect} />
        </HStack>

        <Tabs items={tabItems} selected={selectedTab} onSelect={setSelectedTab} />

        <hr className={style.hr} />
      </div>

      {selectedTab === TabKey.Info && (
        <div className={style.information}>
          <section className={style.section}>
            <h2>オーナー情報</h2>
            <p className={style.info_item}>メール：{email}</p>
            <p className={style.info_item}>登録日：{formattedDate}</p>
            <p className={style.info_label}>内容</p>
            <p className={style.info_content}>{content}</p>
          </section>

          <section className={style.section}>
            <h2>チャンネル情報</h2>
            {selectedChannel && (
              <div className={style.channel_info}>
                <ExImage src={selectedChannel.avatar} title={selectedChannel.name} className={style.channel_avatar} />
                <div className={style.channel_detail}>
                  <span className={style.channel_name}>{selectedChannel.name}</span>
                  <span className={style.channel_count}>登録者数 {selectedChannel.count}</span>
                </div>
              </div>
            )}
            <p className={style.info_label}>説明</p>
            <p className={style.info_content}>{selectedChannel?.description}</p>
          </section>
        </div>
      )}

      {selectedTab === TabKey.Posts && (
        <>
          <MediaIndex title="Video">
            {newMedia.videos.map((item) => (
              <MediaVideo key={item.ulid} media={item} />
            ))}
          </MediaIndex>

          <Divide />
          <MediaIndex title="Music">
            {newMedia.musics.map((item) => (
              <MediaMusic key={item.ulid} media={item} />
            ))}
          </MediaIndex>

          <Divide />
          <MediaIndex title="Comic">
            {newMedia.comics.map((item) => (
              <MediaComic key={item.ulid} media={item} />
            ))}
          </MediaIndex>

          <Divide />
          <MediaIndex title="Picture">
            {newMedia.pictures.map((item) => (
              <MediaPicture key={item.ulid} media={item} />
            ))}
          </MediaIndex>

          <Divide />
          <MediaIndex title="Blog">
            {newMedia.blogs.map((item) => (
              <MediaBlog key={item.ulid} media={item} />
            ))}
          </MediaIndex>

          <Divide />
          <MediaIndex title="Chat">
            {newMedia.chats.map((item) => (
              <MediaChat key={item.ulid} media={item} />
            ))}
          </MediaIndex>
        </>
      )}
      <FollowDeleteModal open={isModal} onClose={handleModal} onAction={handleFollow} avatar={avatar} ulid={ulid} nickname={nickname} followerCount={followerCount} />
    </Main>
  )
}
