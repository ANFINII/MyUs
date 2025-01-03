import { useRouter } from 'next/router'
import { Todo } from 'types/internal/media'
import { getTodos } from 'api/internal/media/list'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginError from 'components/parts/Error/Login'
// import MediaList from 'components/widgets/Media/List/Media'
// import MediaTodo from 'components/widgets/Media/Index/Todo'

interface Props {
  datas: Todo[]
}

export default function Todos(props: Props) {
  const { datas } = props

  const router = useRouter()
  const { search, newDatas } = useNewDatas<Todo[]>({ datas, getDatas: (search) => getTodos(search) })

  return (
    <Main title="Todo" search={{ name: search, count: newDatas.length }}>
      <LoginError margin="mt_24">
        <div className="mt_16">
          <Button color="blue" size="s" name="新規作成" onClick={() => router.push('/media/todo/create')} />
        </div>
        {/* <MediaList medias={newDatas} MediaComponent={MediaTodo} /> */}
      </LoginError>
    </Main>
  )
}
