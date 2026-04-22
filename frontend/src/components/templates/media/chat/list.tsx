import { useRouter } from 'next/router'
import { Chat } from 'types/internal/media/output'
import { PAGE_SIZE } from 'utils/functions/common'
import { useSearch } from 'components/hooks/useSearch'
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

  const router = useRouter()
  const search = useSearch(total)
  const totalPages = Math.ceil(total / PAGE_SIZE)

  const handlePage = (p: number) => {
    router.push({ pathname: router.pathname, query: { ...router.query, page: p } })
  }

  return (
    <Main title="Chat" search={search}>
      <CardList items={datas} Content={ChatCard} />
      <Pagination currentPage={page} totalPages={totalPages} onChange={handlePage} />
    </Main>
  )
}
