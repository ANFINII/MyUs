import { useRouter } from 'next/router'
import { Follow } from 'types/internal/auth'
import { useUser } from 'components/hooks/useUser'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginRequired from 'components/parts/LoginRequired'
import ArticleFollow from 'components/widgets/Article/Follow'

interface Props {
  follows: Follow[]
}

export default function Followers(props: Props) {
  const { follows } = props

  const router = useRouter()
  const { user } = useUser()

  return (
    <Main title="Follower">
      <LoginRequired isAuth={user.isActive}>
        <div className="follow_button">
          <Button color="blue" size="s" name="フォロワー" onClick={() => router.push('/menu/follow')} />
          <span>フォロワー数：{follows.length}</span>
        </div>
        <article className="article_list">
          {follows.map((data) => (
            <ArticleFollow key={data.nickname} follow={data} />
          ))}
        </article>
      </LoginRequired>
    </Main>
  )
}
