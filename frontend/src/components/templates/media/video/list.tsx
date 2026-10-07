import { VideoList } from 'types/internal/media/output'
import { usePagination } from 'components/hooks/usePagination'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import Pagination from 'components/parts/Pagination'
import CardList from 'components/widgets/Card/List'
import VideoCard from 'components/widgets/Card/Media/Video'

interface Props {
  data: VideoList
  page: number
}

export default function Videos(props: Props): React.JSX.Element {
  const { data, page } = props
  const { items, total } = data

  const search = useSearch(total)
  const { currentPage, totalPages, handlePage } = usePagination(total, page)

  return (
    <Main title="Video" search={search}>
      <CardList items={items} Content={VideoCard} />
      <Pagination currentPage={currentPage} totalPages={totalPages} margin="mv_40" onChange={handlePage} />
    </Main>
  )
}
