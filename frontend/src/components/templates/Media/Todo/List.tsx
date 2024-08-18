import { useRouter } from 'next/router'
import { getTodos } from 'api/internal/media/list'
import { Todo } from 'types/internal/media'
import { useNewDatas } from 'components/hooks/useNewList'
import { useUser } from 'components/hooks/useUser'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginRequired from 'components/parts/LoginRequired'
import ArticleTodo from 'components/widgets/Article/Todo'

interface Props {
  datas: Todo[]
}

export default function Todos(props: Props) {
  const { datas } = props

  const router = useRouter()
  const { user } = useUser()
  const { search, newDatas } = useNewDatas<Todo[]>({ datas, getDatas: (search) => getTodos(search) })

  return (
    <Main title="Todo" search={{ name: search, count: newDatas.length }}>
      <LoginRequired isAuth={user.isActive} margin="mt_20">
        <div className="mt_16">
          <Button color="blue" size="s" name="新規作成" onClick={() => router.push('/media/todo/create')} />
        </div>
        <article className="article_list">
          {newDatas.map((data) => (
            <ArticleTodo key={data.id} data={data} />
          ))}
        </article>
      </LoginRequired>
    </Main>
  )
}
