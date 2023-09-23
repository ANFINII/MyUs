import { Search, Media } from 'types/media'
import Comics from 'components/templates/media/comic/list'

const search: Search = {
  name: 'test',
  count: 0,
}
const datas: Media[] = []

export default function ComicsPage() {
  return <Comics search={search} datas={datas} />
}
