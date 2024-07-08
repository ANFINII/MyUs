import { getTodos } from 'api/media/get/list'
import { Todo } from 'types/internal/media'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import ArticleTodo from 'components/widgets/Article/Todo'

interface Props {
  datas: Todo[]
}

export default function Todos(props: Props) {
  const { datas } = props

  const { search, newDatas } = useNewDatas<Todo[]>({ datas, getDatas: (search) => getTodos(search) })

  return (
    <Main title="Todo" search={{ name: search, count: newDatas.length }}>
      <article className="article_list">
        {newDatas.map((data) => (
          <ArticleTodo data={data} key={data.id} />
        ))}
      </article>
    </Main>
  )
}
