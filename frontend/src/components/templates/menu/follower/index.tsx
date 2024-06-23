import Router from 'next/router'
import { Follow } from 'types/internal/auth'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginRequired from 'components/parts/LoginRequired'
import ArticleFollow from 'components/widgets/Article/Follow'

interface Props {
  follows: Follow[]
}

export default function Followers(props: Props) {
  const { follows } = props

  return (
    <Main title="Follower">
      <LoginRequired isAuth>
        <div className="follow_button">
          <Button color="blue" size="s" name="フォロワー" onClick={() => Router.push('/menu/follow')} />
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
