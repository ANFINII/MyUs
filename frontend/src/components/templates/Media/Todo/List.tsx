import { getTodos } from 'api/media/get/list'
import { Todo } from 'types/internal/media'
import { useNewDatas } from 'components/hooks/useNewList'
import { useUser } from 'components/hooks/useUser'
import Main from 'components/layout/Main'
import LoginRequired from 'components/parts/LoginRequired'
import ArticleTodo from 'components/widgets/Article/Todo'

interface Props {
  datas: Todo[]
}

export default function Todos(props: Props) {
  const { datas } = props

  const { user } = useUser()
  const { search, newDatas } = useNewDatas<Todo[]>({ datas, getDatas: (search) => getTodos(search) })

  return (
    <Main title="Todo" search={{ name: search, count: newDatas.length }}>
      <LoginRequired isAuth={user.isActive}>
        <article className="article_list">
          {newDatas.map((data) => (
            <ArticleTodo key={data.id} data={data} />
          ))}
        </article>
      </LoginRequired>
    </Main>
  )
}
