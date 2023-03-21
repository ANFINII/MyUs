import {Query, FollowResponse} from 'utils/type'
import FollowerList from 'components/pages/Follow/FollowerList'

export default function FollowerListPage() {
  const query: Query = {
    name: "test",
    count: 0,
  }
  const datas: Array<FollowResponse> = []
  return (
    <FollowerList is_authenticated={true} query={query} datas={datas} />
  )
}
