import Link from 'next/link'
import { Follow } from 'types/internal/auth'
import ExImage from 'components/parts/ExImage'

interface Props {
  follow: Follow
}

export default function ArticleFollow(props: Props) {
  const { follow } = props
  const { avatar, nickname, introduction, followerCount, followingCount } = follow

  return (
    <section key={nickname} className="section_follow">
      <div className="main_decolation">
        <Link href={`/userpage/${nickname}`} data-name={nickname} className="follow_box">
          <div className="author_follow">
            <ExImage src={avatar} title={nickname} className="follow_image" />
          </div>
          <span title={nickname} className="follow_content_1">
            {nickname}
          </span>
          <span className="follow_content_2">フォロワー数：{followerCount}</span>
          <span className="follow_content_3">フォロー数：{followingCount}</span>
          <div title={introduction} className="follow_content_4">
            {introduction}
          </div>
        </Link>
      </div>
    </section>
  )
}
