import { Search, Media } from 'types/media'
import Todos from 'components/templates/media/todo/list'

const search: Search = {
  name: 'test',
  count: 0,
}
const datas: Media[] = []

export default function TodosPage() {
  return <Todos search={search} datas={datas} />
}
