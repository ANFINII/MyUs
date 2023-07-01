import {Query, ImageResponse} from 'types/media'
import BlogList from 'components/templates/Media/Blog/List'

const query: Query = {
  name: 'test',
  count: 0,
}
const datas: ImageResponse[] = []

export default function BlogListPage() {
  return <BlogList query={query} datas={datas} />
}
