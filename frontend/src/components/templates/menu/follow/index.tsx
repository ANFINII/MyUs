import Router from 'next/router'
import { Follow } from 'types/internal/auth'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginRequired from 'components/parts/LoginRequired'
import ArticleFollow from 'components/widgets/Article/Follow'

interface Props {
  follows: Follow[]
}

export default function Follows(props: Props) {
  const { follows } = props

  return (
    <Main title="Follow">
      <LoginRequired isAuth>
        <div className="follow_button">
          <Button color="blue" size="s" name="フォロー" onClick={() => Router.push('/menu/follower')} />
          <span>フォロー数：{follows.length}</span>
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
