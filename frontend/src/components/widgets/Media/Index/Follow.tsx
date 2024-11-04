import Link from 'next/link'
import { Follow } from 'types/internal/auth'
import ExImage from 'components/parts/ExImage'
import style from './Media.module.scss'

interface Props {
  data: Follow
}

export default function MediaFollow(props: Props) {
  const { data } = props
  const { avatar, nickname, introduction, followerCount, followingCount } = data

  return (
    <section key={nickname} className={style.section_follow}>
      <div className={style.decolation}>
        <Link href={`/userpage/${nickname}`} data-name={nickname} className={style.follow_box}>
          <div className={style.author_follow}>
            <ExImage src={avatar} title={nickname} className={style.follow_image} />
          </div>
          <span title={nickname} className={style.follow_content_1}>
            {nickname}
          </span>
          <span className={style.follow_content_2}>フォロワー数：{followerCount}</span>
          <span className={style.follow_content_3}>フォロー数：{followingCount}</span>
          <div title={introduction} className={style.follow_content_4}>
            {introduction}
          </div>
        </Link>
      </div>
    </section>
  )
}
