import { Chat } from 'types/internal/media/output'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import CardList from 'components/widgets/Card/List'
import ChatCard from 'components/widgets/Card/Media/Chat'

interface Props {
  datas: Chat[]
}

export default function Chats(props: Props): React.JSX.Element {
  const { datas } = props

  const search = useSearch(datas)

  return (
    <Main title="Chat" search={search}>
      <CardList items={datas} Content={ChatCard} />
    </Main>
  )
}
