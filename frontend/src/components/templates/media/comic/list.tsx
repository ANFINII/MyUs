import { Comic } from 'types/internal/media/output'
import { usePagination } from 'components/hooks/usePagination'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import Pagination from 'components/parts/Pagination'
import CardList from 'components/widgets/Card/List'
import ComicCard from 'components/widgets/Card/Media/Comic'

interface Props {
  datas: Comic[]
  total: number
  page: number
}

export default function Comics(props: Props): React.JSX.Element {
  const { datas, total, page } = props

  const search = useSearch(total)
  const { currentPage, totalPages, handlePage } = usePagination(total, page)

  return (
    <Main title="Comic" search={search}>
      <CardList items={datas} Content={ComicCard} />
      <Pagination currentPage={currentPage} totalPages={totalPages} onChange={handlePage} />
    </Main>
  )
}
