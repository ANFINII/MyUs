import { useRouter } from 'next/router'
import { Comic } from 'types/internal/media/output'
import { PAGE_SIZE } from 'utils/functions/common'
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

  const router = useRouter()
  const search = useSearch(total)
  const totalPages = Math.ceil(total / PAGE_SIZE)

  const handlePage = (p: number) => {
    router.push({ pathname: router.pathname, query: { ...router.query, page: p } })
  }

  return (
    <Main title="Comic" search={search}>
      <CardList items={datas} Content={ComicCard} />
      <Pagination currentPage={page} totalPages={totalPages} onChange={handlePage} />
    </Main>
  )
}
