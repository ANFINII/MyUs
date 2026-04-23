import { Music } from 'types/internal/media/output'
import { useSearch } from 'components/hooks/useSearch'
import { useServerPagination } from 'components/hooks/useServerPagination'
import Main from 'components/layout/Main'
import Pagination from 'components/parts/Pagination'
import CardList from 'components/widgets/Card/List'
import MusicCard from 'components/widgets/Card/Media/Music'

interface Props {
  datas: Music[]
  total: number
  page: number
}

export default function Musics(props: Props): React.JSX.Element {
  const { datas, total, page } = props

  const search = useSearch(total)
  const { currentPage, totalPages, handlePage } = useServerPagination(total, page)

  return (
    <Main title="Music" search={search}>
      <CardList items={datas} Content={MusicCard} />
      <Pagination currentPage={currentPage} totalPages={totalPages} onChange={handlePage} />
    </Main>
  )
}
