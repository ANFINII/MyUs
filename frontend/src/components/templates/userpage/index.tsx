import { ChangeEvent, useState } from 'react'
import { Video, Music, Comic, Picture, Blog, Chat } from 'types/internal/media'
import { Option } from 'types/internal/other'
import { UserPage } from 'types/internal/userpage'
import { getUserPageMedia, postFollow } from 'api/internal/user'
import { useUser } from 'components/hooks/useUser'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import ExImage from 'components/parts/ExImage'
import SelectBox from 'components/parts/Input/SelectBox'
import Tabs, { TabItem } from 'components/parts/Tabs'
import FollowButton from 'components/widgets/FollowButton'
import MediaBlog from 'components/widgets/Media/Index/Blog'
import MediaChat from 'components/widgets/Media/Index/Chat'
import MediaComic from 'components/widgets/Media/Index/Comic'
import MediaMusic from 'components/widgets/Media/Index/Music'
import MediaPicture from 'components/widgets/Media/Index/Picture'
import MediaVideo from 'components/widgets/Media/Index/Video'
import MediaIndex from 'components/widgets/Media/List/Index'
import style from './UserPage.module.scss'

const enum TabKey {
  Posts = 'posts',
  Info = 'info',
}

interface Props {
  ulid: string
  userPage: UserPage
}

export default function Userpage(props: Props): React.JSX.Element {
  const { ulid, userPage } = props
  const { avatar, banner, nickname, email, content, dateJoined, channels } = userPage

  const { user } = useUser()
  const [isFollow, setIsFollow] = useState<boolean>(userPage.isFollow)
  const [followerCount, setFollowerCount] = useState<number>(userPage.followerCount)
  const [selected, setSelected] = useState<TabKey>(TabKey.Posts)

  const defaultChannelUlid = channels.find((c) => c.isDefault)?.ulid ?? ''
  const [selectedChannelUlid, setSelectedChannelUlid] = useState<string>(defaultChannelUlid)
  const [videos, setVideos] = useState<Video[]>(userPage.videos)
  const [musics, setMusics] = useState<Music[]>(userPage.musics)
  const [comics, setComics] = useState<Comic[]>(userPage.comics)
  const [pictures, setPictures] = useState<Picture[]>(userPage.pictures)
  const [blogs, setBlogs] = useState<Blog[]>(userPage.blogs)
  const [chats, setChats] = useState<Chat[]>(userPage.chats)

  const isSelf = user.isActive && user.nickname === nickname
  const formattedDate = new Date(dateJoined).toLocaleDateString('ja-JP', { year: 'numeric', month: 'long', day: 'numeric' })

  const tabItems: TabItem<TabKey>[] = [
    { key: TabKey.Posts, label: '投稿' },
    { key: TabKey.Info, label: '情報' },
  ]

  const handleFollow = async () => {
    const ret = await postFollow({ ulid, isFollow: !isFollow })
    if (ret.isErr()) return
    setIsFollow(ret.value.isFollow)
    setFollowerCount(ret.value.followerCount)
  }

  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))

  const handleChannelSelect = async (e: ChangeEvent<HTMLSelectElement>) => {
    const channelUlid = e.target.value
    if (channelUlid === selectedChannelUlid) return
    setSelectedChannelUlid(channelUlid)

    const ret = await getUserPageMedia(ulid, channelUlid)
    if (ret.isErr()) return
    setVideos(ret.value.videos)
    setMusics(ret.value.musics)
    setComics(ret.value.comics)
    setPictures(ret.value.pictures)
    setBlogs(ret.value.blogs)
    setChats(ret.value.chats)
  }

  return (
    <Main metaTitle={`${nickname} - MyUs`}>
      <div className={style.userpage}>
        <figure className={style.banner}>
          <ExImage src={banner} title={nickname} />
        </figure>

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

        <Tabs items={tabItems} selected={selected} onSelect={setSelected} />

        <hr className={style.hr} />
      </div>

      {selected === TabKey.Posts && (
        <>
          <SelectBox label="チャンネル" value={selectedChannelUlid} options={channelOptions} className={style.channel_selector} onChange={handleChannelSelect} />

          <MediaIndex title="Video">
            {videos?.map((media) => (
              <MediaVideo key={media.ulid} media={media} />
            ))}
          </MediaIndex>

          <Divide />
          <MediaIndex title="Music">
            {musics?.map((media) => (
              <MediaMusic key={media.ulid} media={media} />
            ))}
          </MediaIndex>

          <Divide />
          <MediaIndex title="Comic">
            {comics?.map((media) => (
              <MediaComic key={media.ulid} media={media} />
            ))}
          </MediaIndex>

          <Divide />
          <MediaIndex title="Picture">
            {pictures?.map((media) => (
              <MediaPicture key={media.ulid} media={media} />
            ))}
          </MediaIndex>

          <Divide />
          <MediaIndex title="Blog">
            {blogs?.map((media) => (
              <MediaBlog key={media.ulid} media={media} />
            ))}
          </MediaIndex>

          <Divide />
          <MediaIndex title="Chat">
            {chats?.map((media) => (
              <MediaChat key={media.ulid} media={media} />
            ))}
          </MediaIndex>
        </>
      )}

      {selected === TabKey.Info && (
        <div className={style.information}>
          <h1>チャンネル情報</h1>
          <p className={style.info_label}>概要</p>
          <p className={style.info_content}>{content}</p>
          <p>メール：{email}</p>
          <p>登録日：{formattedDate}</p>
        </div>
      )}
    </Main>
  )
}
