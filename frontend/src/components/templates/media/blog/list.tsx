import { Blog } from 'types/internal/media/output'
import { usePagination } from 'components/hooks/usePagination'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import Pagination from 'components/parts/Pagination'
import CardList from 'components/widgets/Card/List'
import BlogCard from 'components/widgets/Card/Media/Blog'

interface Props {
  datas: Blog[]
  total: number
  page: number
}

export default function Blogs(props: Props): React.JSX.Element {
  const { datas, total, page } = props

  const search = useSearch(total)
  const { currentPage, totalPages, handlePage } = usePagination(total, page)

  return (
    <Main title="Blog" search={search}>
      <CardList items={datas} Content={BlogCard} />
      <Pagination currentPage={currentPage} totalPages={totalPages} onChange={handlePage} />
    </Main>
  )
}
