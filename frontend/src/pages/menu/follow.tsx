import { Search, Follow } from 'types/internal/media'
import Follows from 'components/templates/follow/FollowList'

const search: Search = {
  name: 'test',
  count: 0,
}
const datas: Follow[] = []

export default function FollowsPage() {
  return <Follows isAuth={true} search={search} datas={datas} />
}
