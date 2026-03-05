import { useState } from 'react'
import { UserPage } from 'types/internal/userpage'
import { postFollow } from 'api/internal/user'
import { useUser } from 'components/hooks/useUser'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import ExImage from 'components/parts/ExImage'
import FollowButton from 'components/widgets/FollowButton'
import MediaBlog from 'components/widgets/Media/Index/Blog'
import MediaChat from 'components/widgets/Media/Index/Chat'
import MediaComic from 'components/widgets/Media/Index/Comic'
import MediaMusic from 'components/widgets/Media/Index/Music'
import MediaPicture from 'components/widgets/Media/Index/Picture'
import MediaVideo from 'components/widgets/Media/Index/Video'
import MediaIndex from 'components/widgets/Media/List/Index'
import style from './UserPage.module.scss'

type TabType = 'posts' | 'info'

interface Props {
  ulid: string
  userPage: UserPage
}

export default function Userpage(props: Props): React.JSX.Element {
  const { ulid, userPage } = props
  const { avatar, banner, nickname, email, content, dateJoined, videos, musics, comics, pictures, blogs, chats } = userPage

  const { user } = useUser()
  const [isFollow, setIsFollow] = useState(userPage.isFollow)
  const [followerCount, setFollowerCount] = useState(userPage.followerCount)
  const [activeTab, setActiveTab] = useState<TabType>('posts')

  const handleFollow = async () => {
    const ret = await postFollow({ ulid, isFollow: !isFollow })
    if (ret.isOk()) {
      setIsFollow(ret.value.isFollow)
      setFollowerCount(ret.value.followerCount)
    }
  }

  const isSelf = user.isActive && user.nickname === nickname
  const formattedDate = new Date(dateJoined).toLocaleDateString('ja-JP', { year: 'numeric', month: 'long', day: 'numeric' })

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

        <div className={style.tabs}>
          <a className={activeTab === 'posts' ? style.active : ''} onClick={() => setActiveTab('posts')}>
            投稿
          </a>
          <a className={activeTab === 'info' ? style.active : ''} onClick={() => setActiveTab('info')}>
            情報
          </a>
        </div>

        <hr className={style.hr} />
      </div>

      {activeTab === 'posts' && (
        <>
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

      {activeTab === 'info' && (
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
