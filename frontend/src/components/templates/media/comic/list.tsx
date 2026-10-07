import { ComicList } from 'types/internal/media/output'
import { usePagination } from 'components/hooks/usePagination'
import { useSearchResult } from 'components/hooks/useSearchResult'
import Main from 'components/layout/Main'
import Pagination from 'components/parts/Pagination'
import CardList from 'components/widgets/Card/List'
import ComicCard from 'components/widgets/Card/Media/Comic'

interface Props {
  data: ComicList
  page: number
}

export default function Comics(props: Props): React.JSX.Element {
  const { data, page } = props
  const { items, total } = data

  const search = useSearchResult(total)
  const { currentPage, totalPages, handlePage } = usePagination(total, page)

  return (
    <Main title="Comic" search={search}>
      <CardList items={items} Content={ComicCard} />
      <Pagination currentPage={currentPage} totalPages={totalPages} margin="mv_40" onChange={handlePage} />
    </Main>
  )
}
