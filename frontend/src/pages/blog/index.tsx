import {Query, ImageResponse} from 'utils/type'
import BlogList from 'components/pages/Media/Blog/List'

export default function BlogListPage() {
  const query: Query = {
    name: "test",
    count: 0,
  }
  const datas: Array<ImageResponse> = []
  return (
    <BlogList query={query} datas={datas} />
  )
}
