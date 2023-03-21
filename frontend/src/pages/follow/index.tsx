import {Query, FollowResponse} from 'utils/type'
import FollowList from 'components/pages/Follow/FollowList'

export default function FollowListPage() {
  const query: Query = {
    name: "test",
    count: 0,
  }
  const datas: Array<FollowResponse> = []
  return (
    <FollowList is_authenticated={true} query={query} datas={datas} />
  )
}
