import { ChatList } from 'types/internal/media/output'
import { usePagination } from 'components/hooks/usePagination'
import { useSearchResult } from 'components/hooks/useSearchResult'
import Main from 'components/layout/Main'
import Pagination from 'components/parts/Pagination'
import CardList from 'components/widgets/Card/List'
import ChatCard from 'components/widgets/Card/Media/Chat'

interface Props {
  data: ChatList
  page: number
}

export default function Chats(props: Props): React.JSX.Element {
  const { data, page } = props
  const { items, total } = data

  const search = useSearchResult(total)
  const { currentPage, totalPages, handlePage } = usePagination(total, page)

  return (
    <Main title="Chat" search={search}>
      <CardList items={items} Content={ChatCard} />
      <Pagination currentPage={currentPage} totalPages={totalPages} margin="mv_40" onChange={handlePage} />
    </Main>
  )
}
