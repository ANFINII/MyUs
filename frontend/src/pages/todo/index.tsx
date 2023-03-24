import {Query, MediaResponse} from 'utils/type'
import TodoList from 'components/pages/Media/Todo/List'

const query: Query = {
  name: "test",
  count: 0,
}
const datas: Array<MediaResponse> = []

export default function TodoListPage() {
  return (
    <TodoList query={query} datas={datas} />
  )
}
