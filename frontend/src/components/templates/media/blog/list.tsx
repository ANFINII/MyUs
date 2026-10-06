import { BlogList } from 'types/internal/media/output'
import { usePagination } from 'components/hooks/usePagination'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import Pagination from 'components/parts/Pagination'
import CardList from 'components/widgets/Card/List'
import BlogCard from 'components/widgets/Card/Media/Blog'

interface Props {
  list: BlogList
  page: number
}

export default function Blogs(props: Props): React.JSX.Element {
  const { list, page } = props
  const { datas, total } = list

  const search = useSearch(total)
  const { currentPage, totalPages, handlePage } = usePagination(total, page)

  return (
    <Main title="Blog" search={search}>
      <CardList items={datas} Content={BlogCard} />
      <Pagination currentPage={currentPage} totalPages={totalPages} margin="mv_40" onChange={handlePage} />
    </Main>
  )
}
