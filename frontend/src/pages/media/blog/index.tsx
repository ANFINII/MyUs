import { Search, ImageResponse } from 'types/media'
import Blogs from 'components/templates/media/blog/List'

const search: Search = {
  name: 'test',
  count: 0,
}
const datas: ImageResponse[] = []

export default function BlogsPage() {
  return <Blogs search={search} datas={datas} />
}
