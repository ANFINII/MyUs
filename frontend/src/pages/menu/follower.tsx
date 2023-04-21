import {Query, FollowResponse} from 'utils/type'
import FollowerList from 'components/templates/Follow/FollowerList'

const query: Query = {
  name: 'test',
  count: 0,
}
const datas: Array<FollowResponse> = []

export default function FollowerListPage() {
  return <FollowerList is_authenticated={true} query={query} datas={datas} />
}
