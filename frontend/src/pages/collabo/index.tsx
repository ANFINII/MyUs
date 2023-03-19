import {Query, MediaResponse} from 'utils/type'
import CollaboList from 'components/pages/Media/Collabo/List'

export default function CollaboListPage() {
  const query: Query = {
    name: "test",
    count: 0,
  }
  const datas: Array<MediaResponse> = []
  return (
    <CollaboList query={query} datas={datas} />
  )
}
