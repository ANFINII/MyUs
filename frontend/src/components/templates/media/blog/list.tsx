import { useRouter } from 'next/router'
import { Blog } from 'types/internal/media/output'
import { PAGE_SIZE } from 'utils/functions/common'
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

  const router = useRouter()
  const search = useSearch(total)
  const totalPages = Math.ceil(total / PAGE_SIZE)

  const handlePage = (p: number) => {
    router.push({ pathname: router.pathname, query: { ...router.query, page: p } })
  }

  return (
    <Main title="Blog" search={search}>
      <CardList items={datas} Content={BlogCard} />
      <Pagination currentPage={page} totalPages={totalPages} onChange={handlePage} />
    </Main>
  )
}
