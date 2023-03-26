import {Query, FollowResponse} from 'utils/type'
import FollowList from 'components/pages/Follow/FollowList'

const query: Query = {
  name: "test",
  count: 0,
}
const datas: Array<FollowResponse> = []

export default function FollowListPage() {
  return (
    <FollowList is_authenticated={true} query={query} datas={datas} />
  )
}
