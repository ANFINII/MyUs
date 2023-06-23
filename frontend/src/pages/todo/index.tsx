import {Query, MediaResponse} from 'utils/type'
import TodoList from 'components/templates/Media/Todo/List'

const query: Query = {
  name: 'test',
  count: 0,
}
const datas: MediaResponse[] = []

export default function TodoListPage() {
  return <TodoList query={query} datas={datas} />
}
