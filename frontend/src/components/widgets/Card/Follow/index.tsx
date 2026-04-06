import Link from 'next/link'
import { Follow } from 'types/internal/user'
import Card from 'components/parts/Card'
import ExImage from 'components/parts/ExImage'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import style from './Follow.module.scss'

interface Props {
  item: Follow
}

export default function FollowCard(props: Props): React.JSX.Element {
  const { item } = props
  const { avatar, ulid, nickname, introduction, followerCount, followingCount } = item

  return (
    <Card className={style.card}>
      <Link href={`/userpage/${ulid}`} className={style.box}>
        <HStack gap="5">
          <ExImage src={avatar} title={nickname} className={style.image} />
          <VStack gap="1" className="fs_12">
            <span title={nickname}>{nickname}</span>
            <span>フォロワー数：{followerCount}</span>
            <span>
              フォロー数<span className="ml_12">：{followingCount}</span>
            </span>
          </VStack>
        </HStack>
        <div title={introduction} className={style.introduction}>
          {introduction}
        </div>
      </Link>
    </Card>
  )
}
