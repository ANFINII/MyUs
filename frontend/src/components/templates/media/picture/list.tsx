import { Picture } from 'types/internal/media/output'
import { useSearch } from 'components/hooks/useSearch'
import { useServerPagination } from 'components/hooks/useServerPagination'
import Main from 'components/layout/Main'
import Pagination from 'components/parts/Pagination'
import CardList from 'components/widgets/Card/List'
import PictureCard from 'components/widgets/Card/Media/Picture'

interface Props {
  datas: Picture[]
  total: number
  page: number
}

export default function Pictures(props: Props): React.JSX.Element {
  const { datas, total, page } = props

  const search = useSearch(total)
  const { currentPage, totalPages, handlePage } = useServerPagination(total, page)

  return (
    <Main title="Picture" search={search}>
      <CardList items={datas} Content={PictureCard} />
      <Pagination currentPage={currentPage} totalPages={totalPages} onChange={handlePage} />
    </Main>
  )
}
