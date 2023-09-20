import { Search, ImageResponse } from 'types/media'
import Pictures from 'components/templates/media/picture/List'

const search: Search = {
  name: 'test',
  count: 0,
}
const datas: ImageResponse[] = []

export default function PicturesPage() {
  return <Pictures search={search} datas={datas} />
}
