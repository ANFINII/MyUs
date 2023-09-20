import { Search, FollowResponse } from 'types/media'
import Followers from 'components/templates/follow/FollowerList'

const search: Search = {
  name: 'test',
  count: 0,
}
const datas: FollowResponse[] = []

export default function FollowersPage() {
  return <Followers isAuthenticated={true} search={search} datas={datas} />
}
