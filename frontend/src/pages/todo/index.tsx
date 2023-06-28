import { SearchQuery, MediaResponse } from 'types/media'
import TodoList from 'components/templates/Media/Todo/List'

const query: SearchQuery = {
  name: 'test',
  count: 0,
}
const datas: MediaResponse[] = []

export default function TodoListPage() {
  return <TodoList query={query} datas={datas} />
}
