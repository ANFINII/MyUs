import { Video } from 'types/internal/media/output'
import { useSearch } from 'components/hooks/useSearch'
import { useServerPagination } from 'components/hooks/useServerPagination'
import Main from 'components/layout/Main'
import Pagination from 'components/parts/Pagination'
import CardList from 'components/widgets/Card/List'
import VideoCard from 'components/widgets/Card/Media/Video'

interface Props {
  datas: Video[]
  total: number
  page: number
}

export default function Videos(props: Props): React.JSX.Element {
  const { datas, total, page } = props

  const search = useSearch(total)
  const { currentPage, totalPages, handlePage } = useServerPagination(total, page)

  return (
    <Main title="Video" search={search}>
      <CardList items={datas} Content={VideoCard} />
      <Pagination currentPage={currentPage} totalPages={totalPages} onChange={handlePage} />
    </Main>
  )
}
