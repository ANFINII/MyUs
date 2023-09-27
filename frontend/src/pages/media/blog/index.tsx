import { Search, Picture } from 'types/internal/media'
import Blogs from 'components/templates/media/blog/list'

const search: Search = {
  name: 'test',
  count: 0,
}
const datas: Picture[] = []

export default function BlogsPage() {
  return <Blogs search={search} datas={datas} />
}
