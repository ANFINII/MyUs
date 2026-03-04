import { useState } from 'react'
import { UserPage } from 'types/internal/userpage'
import { postFollow } from 'api/internal/user'
import { useUser } from 'components/hooks/useUser'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Divide from 'components/parts/Divide'
import ExImage from 'components/parts/ExImage'
import MediaBlog from 'components/widgets/Media/Index/Blog'
import MediaChat from 'components/widgets/Media/Index/Chat'
import MediaComic from 'components/widgets/Media/Index/Comic'
import MediaMusic from 'components/widgets/Media/Index/Music'
import MediaPicture from 'components/widgets/Media/Index/Picture'
import MediaVideo from 'components/widgets/Media/Index/Video'
import MediaIndex from 'components/widgets/Media/List/Index'
import style from './UserPage.module.scss'

interface Props {
  ulid: string
  userPage: UserPage
}

export default function Userpage(props: Props): React.JSX.Element {
  const { ulid, userPage } = props
  const { avatar, banner, nickname, content, videos, musics, comics, pictures, blogs, chats } = userPage

  const { user } = useUser()
  const [isFollow, setIsFollow] = useState(userPage.isFollow)
  const [followerCount, setFollowerCount] = useState(userPage.followerCount)

  const handleFollow = async () => {
    const ret = await postFollow({ ulid, isFollow: !isFollow })
    if (ret.isOk()) {
      setIsFollow(ret.value.isFollow)
      setFollowerCount(ret.value.followerCount)
    }
  }

  const isSelf = user.isActive && user.nickname === nickname

  return (
    <Main metaTitle={`${nickname} - MyUs`}>
      <div className={style.userpage}>
        <div className={style.banner}>
          <ExImage src={banner} title={nickname} />
        </div>

        <div className={style.profile}>
          <ExImage src={avatar} title={nickname} className={style.avatar} />
          <div className={style.info}>
            <span className={style.nickname}>{nickname}</span>
            <div className={style.counts}>
              <span>フォロワー数 {followerCount}</span>
              <span>フォロー数 {userPage.followingCount}</span>
            </div>
            {content && <p>{content}</p>}
          </div>
          {isSelf ? (
            <Button name="フォローする" color="green" disabled />
          ) : user.isActive ? (
            <Button name={isFollow ? '解除する' : 'フォローする'} color={isFollow ? 'red' : 'green'} onClick={handleFollow} />
          ) : (
            <Button name="フォローする" color="green" disabled />
          )}
        </div>
      </div>

      <Divide />
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
    </Main>
  )
}
