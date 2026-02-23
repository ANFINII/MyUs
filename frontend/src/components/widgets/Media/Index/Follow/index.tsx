import Link from 'next/link'
import { Follow } from 'types/internal/user'
import ExImage from 'components/parts/ExImage'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import style from './Follow.module.scss'

interface Props {
  media: Follow
}

export default function MediaFollow(props: Props): React.JSX.Element {
  const { media } = props
  const { avatar, ulid, nickname, introduction, followerCount, followingCount } = media

  return (
    <section key={ulid} className={style.media_follow}>
      <Link href={`/userpage/${ulid}`} className={style.follow_box}>
        <HStack gap="5">
          <ExImage src={avatar} title={nickname} className={style.follow_image} />
          <VStack gap="1" className="fs_12">
            <span title={nickname}>{nickname}</span>
            <span>フォロワー数：{followerCount}</span>
            <span>
              フォロー数<span className="ml_12">：{followingCount}</span>
            </span>
          </VStack>
        </HStack>
        <div title={introduction} className={style.follow_introduction}>
          {introduction}
        </div>
      </Link>
    </section>
  )
}
