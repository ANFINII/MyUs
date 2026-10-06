import { PictureList } from 'types/internal/media/output'
import { usePagination } from 'components/hooks/usePagination'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import Pagination from 'components/parts/Pagination'
import CardList from 'components/widgets/Card/List'
import PictureCard from 'components/widgets/Card/Media/Picture'

interface Props {
  list: PictureList
  page: number
}

export default function Pictures(props: Props): React.JSX.Element {
  const { list, page } = props
  const { datas, total } = list

  const search = useSearch(total)
  const { currentPage, totalPages, handlePage } = usePagination(total, page)

  return (
    <Main title="Picture" search={search}>
      <CardList items={datas} Content={PictureCard} />
      <Pagination currentPage={currentPage} totalPages={totalPages} margin="mv_40" onChange={handlePage} />
    </Main>
  )
}
