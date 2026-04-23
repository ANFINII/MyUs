import { useRouter } from 'next/router'
import { Music } from 'types/internal/media/output'
import { PAGE_SIZE } from 'utils/functions/common'
import { useSearch } from 'components/hooks/useSearch'
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

  const router = useRouter()
  const search = useSearch(total)
  const totalPages = Math.ceil(total / PAGE_SIZE)

  const handlePage = (p: number) => {
    router.push({ pathname: router.pathname, query: { ...router.query, page: p } })
  }

  return (
    <Main title="Music" search={search}>
      <CardList items={datas} Content={MusicCard} />
      <Pagination currentPage={page} totalPages={totalPages} onChange={handlePage} />
    </Main>
  )
}
