import { Query, FollowResponse } from 'types/media'
import FollowList from 'components/templates/Follow/FollowList'

const query: Query = {
  name: 'test',
  count: 0,
}
const datas: FollowResponse[] = []

export default function FollowListPage() {
  return <FollowList isAuthenticated={true} query={query} datas={datas} />
}
