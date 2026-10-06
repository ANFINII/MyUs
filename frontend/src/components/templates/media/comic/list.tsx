import { ComicList } from 'types/internal/media/output'
import { usePagination } from 'components/hooks/usePagination'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import Pagination from 'components/parts/Pagination'
import CardList from 'components/widgets/Card/List'
import ComicCard from 'components/widgets/Card/Media/Comic'

interface Props {
  list: ComicList
  page: number
}

export default function Comics(props: Props): React.JSX.Element {
  const { list, page } = props
  const { datas, total } = list

  const search = useSearch(total)
  const { currentPage, totalPages, handlePage } = usePagination(total, page)

  return (
    <Main title="Comic" search={search}>
      <CardList items={datas} Content={ComicCard} />
      <Pagination currentPage={currentPage} totalPages={totalPages} margin="mv_40" onChange={handlePage} />
    </Main>
  )
}
