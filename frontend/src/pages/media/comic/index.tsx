import { Search, Picture } from 'types/internal/media'
import Comics from 'components/templates/media/comic/list'

const search: Search = {
  name: 'test',
  count: 0,
}
const datas: Picture[] = []

export default function ComicsPage() {
  return <Comics search={search} datas={datas} />
}
