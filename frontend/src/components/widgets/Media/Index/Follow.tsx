import Link from 'next/link'
import { Follow } from 'types/internal/auth'
import ExImage from 'components/parts/ExImage'
import style from './Follow.module.scss'
import Horizontal from 'components/parts/Stack/Horizontal'
import Vertical from 'components/parts/Stack/Vertical'

interface Props {
  media: Follow
}

export default function MediaFollow(props: Props) {
  const { media } = props
  const { avatar, nickname, introduction, followerCount, followingCount } = media

  return (
    <section key={nickname} className={style.media_follow}>
      <Link href={`/userpage/${nickname}`} className={style.follow_box}>
        <Horizontal gap="5">
          <ExImage src={avatar} title={nickname} className={style.follow_image} />
          <Vertical gap="1" className="fs_12">
            <span title={nickname}>{nickname}</span>
            <span>フォロワー数：{followerCount}</span>
            <span>
              フォロー数<span className="ml_12">：{followingCount}</span>
            </span>
          </Vertical>
        </Horizontal>
        <div title={introduction} className={style.follow_introduction}>
          {introduction}
        </div>
      </Link>
    </section>
  )
}
