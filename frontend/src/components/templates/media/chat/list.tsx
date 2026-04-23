import { Chat } from 'types/internal/media/output'
import { useSearch } from 'components/hooks/useSearch'
import { useServerPagination } from 'components/hooks/useServerPagination'
import Main from 'components/layout/Main'
import Pagination from 'components/parts/Pagination'
import CardList from 'components/widgets/Card/List'
import ChatCard from 'components/widgets/Card/Media/Chat'

interface Props {
  datas: Chat[]
  total: number
  page: number
}

export default function Chats(props: Props): React.JSX.Element {
  const { datas, total, page } = props

  const search = useSearch(total)
  const { currentPage, totalPages, handlePage } = useServerPagination(total, page)

  return (
    <Main title="Chat" search={search}>
      <CardList items={datas} Content={ChatCard} />
      <Pagination currentPage={currentPage} totalPages={totalPages} onChange={handlePage} />
    </Main>
  )
}
