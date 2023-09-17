import { Query, ImageResponse } from 'types/media'
import PictureList from 'components/templates/Media/Picture/List'

const query: Query = {
  name: 'test',
  count: 0,
}
const datas: ImageResponse[] = []

export default function PictureListPage() {
  return <PictureList query={query} datas={datas} />
}
