import {Query, MediaResponse} from 'types/media'
import ComicList from 'components/templates/Media/Comic/List'

const query: Query = {
  name: 'test',
  count: 0,
}
const datas: Array<MediaResponse> = []

export default function ComicListPage() {
  return <ComicList query={query} datas={datas} />
}
