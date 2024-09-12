import { useRouter } from 'next/router'
import { getFollow } from 'api/internal/user'
import { Follow } from 'types/internal/auth'
import { useNewDatas } from 'components/hooks/useNewList'
import { useUser } from 'components/hooks/useUser'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginRequired from 'components/parts/LoginRequired'
import ArticleFollow from 'components/widgets/Article/Follow'

interface Props {
  follows: Follow[]
}

export default function Follows(props: Props) {
  const { follows } = props

  const router = useRouter()
  const { user } = useUser()
  const { search, newDatas } = useNewDatas<Follow[]>({ datas: follows, getDatas: (search) => getFollow(search) })

  return (
    <Main title="Follow" search={{ name: search, count: newDatas.length }}>
      <LoginRequired isAuth={user.isActive} margin="mt_24">
        <div className="mt_16">
          <Button color="blue" size="s" name="フォロー" onClick={() => router.push('/menu/follower')} />
          <span className="ml_8">フォロー数：{follows.length}</span>
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
