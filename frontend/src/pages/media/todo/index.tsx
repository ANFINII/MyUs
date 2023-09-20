import { Search, MediaResponse } from 'types/media'
import Todos from 'components/templates/media/todo/List'

const search: Search = {
  name: 'test',
  count: 0,
}
const datas: MediaResponse[] = []

export default function TodosPage() {
  return <Todos search={search} datas={datas} />
}
