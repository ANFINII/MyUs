import { Blog } from 'types/internal/media/output'
import { useSearch } from 'components/hooks/useSearch'
import { useServerPagination } from 'components/hooks/useServerPagination'
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
  const { currentPage, totalPages, handlePage } = useServerPagination(total, page)

  return (
    <Main title="Blog" search={search}>
      <CardList items={datas} Content={BlogCard} />
      <Pagination currentPage={currentPage} totalPages={totalPages} onChange={handlePage} />
    </Main>
  )
}
