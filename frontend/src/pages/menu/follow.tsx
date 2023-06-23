import {Query, FollowResponse} from 'utils/type'
import FollowList from 'components/templates/Follow/FollowList'

const query: Query = {
  name: 'test',
  count: 0,
}
const datas: FollowResponse[] = []

export default function FollowListPage() {
  return <FollowList is_authenticated={true} query={query} datas={datas} />
}
