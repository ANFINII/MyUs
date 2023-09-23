import { Search, Picture } from 'types/media'
import Pictures from 'components/templates/media/picture/list'

const search: Search = {
  name: 'test',
  count: 0,
}
const datas: Picture[] = []

export default function PicturesPage() {
  return <Pictures search={search} datas={datas} />
}
