import {Query, ImageResponse} from 'utils/type'
import PictureList from 'components/pages/Media/Picture/List'

const query: Query = {
  name: 'test',
  count: 0,
}
const datas: Array<ImageResponse> = []

export default function PictureListPage() {
  return <PictureList query={query} datas={datas} />
}
