import {Query, ImageResponse} from 'utils/type'
import PictureList from 'components/pages/Media/Picture/List'

export default function PictureListPage() {
  const query: Query = {
    name: "test",
    count: 0,
  }
  const datas: Array<ImageResponse> = []
  return (
    <PictureList query={query} datas={datas} />
  )
}
