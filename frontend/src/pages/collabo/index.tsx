import {Query, MediaResponse} from 'utils/type'
import CollaboList from 'components/templates/Media/Collabo/List'

const query: Query = {
  name: 'test',
  count: 0,
}
const datas: Array<MediaResponse> = []

export default function CollaboListPage() {
  return <CollaboList query={query} datas={datas} />
}
