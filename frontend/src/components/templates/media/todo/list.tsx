import { useRouter } from 'next/router'
import { getTodos } from 'api/internal/media/list'
import { Todo } from 'types/internal/media'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginRequired from 'components/parts/LoginRequired'
import ArticleMedia from 'components/widgets/Media/Article/Media'
import SectionTodo from 'components/widgets/Media/Section/Todo'

interface Props {
  datas: Todo[]
}

export default function Todos(props: Props) {
  const { datas } = props

  const router = useRouter()
  const { search, newDatas } = useNewDatas<Todo[]>({ datas, getDatas: (search) => getTodos(search) })

  return (
    <Main title="Todo" search={{ name: search, count: newDatas.length }}>
      <LoginRequired margin="mt_24">
        <div className="mt_16">
          <Button color="blue" size="s" name="新規作成" onClick={() => router.push('/media/todo/create')} />
        </div>
        <ArticleMedia datas={newDatas} SectionMedia={SectionTodo} />
      </LoginRequired>
    </Main>
  )
}
