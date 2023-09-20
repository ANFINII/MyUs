import { Search, FollowResponse } from 'types/media'
import Follows from 'components/templates/follow/FollowList'

const search: Search = {
  name: 'test',
  count: 0,
}
const datas: FollowResponse[] = []

export default function FollowsPage() {
  return <Follows isAuthenticated={true} search={search} datas={datas} />
}
