import { Search, Follow } from 'types/internal/media'
import Followers from 'components/templates/menu/follower'

const search: Search = {
  name: 'test',
  count: 0,
}
const datas: Follow[] = []

export default function FollowersPage() {
  return <Followers search={search} datas={datas} />
}
