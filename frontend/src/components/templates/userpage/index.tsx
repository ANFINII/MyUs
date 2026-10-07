import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useNavigate } from '@tanstack/react-router'
import { Option } from 'types/internal/other'
import { UserPage, UserPageMedia } from 'types/internal/userpage'
import { postFollow } from 'api/internal/user'
import { useUser } from 'components/hooks/useUser'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import ExImage from 'components/parts/ExImage'
import SelectBox from 'components/parts/Input/SelectBox'
import HStack from 'components/parts/Stack/Horizontal'
import Tabs, { TabItem } from 'components/parts/Tabs'
import CardIndexList from 'components/widgets/Card/IndexList'
import BlogCard from 'components/widgets/Card/Media/Blog'
import ChatCard from 'components/widgets/Card/Media/Chat'
import ComicCard from 'components/widgets/Card/Media/Comic'
import MusicCard from 'components/widgets/Card/Media/Music'
import PictureCard from 'components/widgets/Card/Media/Picture'
import VideoCard from 'components/widgets/Card/Media/Video'
import FollowButton from 'components/widgets/FollowButton'
import FollowDeleteModal from 'components/widgets/Modal/FollowDelete'
import style from './UserPage.module.scss'

const enum TabKey {
  Info = 'info',
  Posts = 'posts',
}

interface Props {
  ulid: string
  channelUlid: string
  userPage: UserPage
  media: UserPageMedia
}

export default function Userpage(props: Props): React.JSX.Element {
  const { ulid, channelUlid, userPage, media } = props
  const { avatar, banner, nickname, email, content, dateJoined, channels } = userPage

  const navigate = useNavigate()
  const { t, i18n } = useTranslation()
  const { user } = useUser()
  const [isModal, setIsModal] = useState<boolean>(false)
  const [isFollow, setIsFollow] = useState<boolean>(userPage.isFollow)
  const [selectedTab, setSelectedTab] = useState<TabKey>(TabKey.Info)
  const [followerCount, setFollowerCount] = useState<number>(userPage.followerCount)

  const isSelf = user.isActive && user.nickname === nickname
  const formattedDate = new Date(dateJoined).toLocaleDateString(i18n.language, { year: 'numeric', month: 'long', day: 'numeric' })
  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))
  const selectedChannel = channels.find((c) => c.ulid === channelUlid)

  const tabItems: TabItem<TabKey>[] = [
    { key: TabKey.Info, label: t('media.userpage.info') },
    { key: TabKey.Posts, label: t('media.userpage.posts') },
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

  const handleChannelSelect = (e: ChangeEvent<HTMLSelectElement>) => {
    navigate({ to: '/userpage/$ulid', params: { ulid }, search: { channel: e.target.value }, replace: true })
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
              <span className={style.follower}>{t('media.userpage.follower', { count: followerCount })}</span>
              <span className={style.following}>{t('media.userpage.following', { count: userPage.followingCount })}</span>
            </div>
            <span className={style.follow_button}>
              <FollowButton isFollow={isFollow} disabled={isSelf || !user.isActive} onClick={handleFollow} />
            </span>
          </div>
          <SelectBox label={t('media.userpage.channel')} value={channelUlid} options={channelOptions} className={style.channel} onChange={handleChannelSelect} />
        </HStack>

        <Tabs items={tabItems} selected={selectedTab} onSelect={setSelectedTab} />

        <hr className={style.hr} />
      </div>

      {selectedTab === TabKey.Info && (
        <div className={style.information}>
          <section className={style.section}>
            <h2>{t('media.userpage.ownerInfo')}</h2>
            <p className={style.info_item}>{t('media.userpage.email', { email })}</p>
            <p className={style.info_item}>{t('media.userpage.joined', { date: formattedDate })}</p>
            <p className={style.info_label}>{t('media.userpage.content')}</p>
            <p className={style.info_content}>{content}</p>
          </section>

          <section className={style.section}>
            <h2>{t('media.userpage.channelInfo')}</h2>
            {selectedChannel && (
              <div className={style.channel_info}>
                <ExImage src={selectedChannel.avatar} title={selectedChannel.name} className={style.channel_avatar} />
                <div className={style.channel_detail}>
                  <span className={style.channel_name}>{selectedChannel.name}</span>
                  <span className={style.channel_count}>{t('media.userpage.subscriber', { count: selectedChannel.count })}</span>
                </div>
              </div>
            )}
            <p className={style.info_label}>{t('media.userpage.description')}</p>
            <p className={style.info_content}>{selectedChannel?.description}</p>
          </section>
        </div>
      )}

      {selectedTab === TabKey.Posts && (
        <>
          <CardIndexList title="Video">
            {media.videos.map((item) => (
              <VideoCard key={item.ulid} item={item} />
            ))}
          </CardIndexList>

          <Divide />
          <CardIndexList title="Music">
            {media.musics.map((item) => (
              <MusicCard key={item.ulid} item={item} />
            ))}
          </CardIndexList>

          <Divide />
          <CardIndexList title="Blog">
            {media.blogs.map((item) => (
              <BlogCard key={item.ulid} item={item} />
            ))}
          </CardIndexList>

          <Divide />
          <CardIndexList title="Comic">
            {media.comics.map((item) => (
              <ComicCard key={item.ulid} item={item} />
            ))}
          </CardIndexList>

          <Divide />
          <CardIndexList title="Picture">
            {media.pictures.map((item) => (
              <PictureCard key={item.ulid} item={item} />
            ))}
          </CardIndexList>

          <Divide />
          <CardIndexList title="Chat">
            {media.chats.map((item) => (
              <ChatCard key={item.ulid} item={item} />
            ))}
          </CardIndexList>
        </>
      )}
      <FollowDeleteModal open={isModal} onClose={handleModal} onAction={handleFollow} avatar={avatar} ulid={ulid} nickname={nickname} followerCount={followerCount} />
    </Main>
  )
}
