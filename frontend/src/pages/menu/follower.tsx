import { Query, FollowResponse } from 'types/media'
import FollowerList from 'components/templates/Follow/FollowerList'

const query: Query = {
  name: 'test',
  count: 0,
}
const datas: FollowResponse[] = []

export default function FollowerListPage() {
  return <FollowerList isAuthenticated={true} query={query} datas={datas} />
}
