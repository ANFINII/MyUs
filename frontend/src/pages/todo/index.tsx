import {Query, MediaResponse} from 'utils/type'
import TodoList from 'components/pages/Media/Todo/List'

export default function TodoListPage() {
  const query: Query = {
    name: "test",
    count: 0,
  }
  const datas: Array<MediaResponse> = []
  return (
    <TodoList query={query} datas={datas} />
  )
}
