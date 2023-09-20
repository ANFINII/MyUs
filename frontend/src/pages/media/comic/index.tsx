import { Search, MediaResponse } from 'types/media'
import Comics from 'components/templates/media/comic/List'

const search: Search = {
  name: 'test',
  count: 0,
}
const datas: Array<MediaResponse> = []

export default function ComicsPage() {
  return <Comics search={search} datas={datas} />
}
