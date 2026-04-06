import { Chat } from 'types/internal/media'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import ChatCard from 'components/widgets/Card/Chat'
import CardList from 'components/widgets/Card/List'

interface Props {
  datas: Chat[]
}

export default function Chats(props: Props): React.JSX.Element {
  const { datas } = props

  const search = useSearch(datas)

  return (
    <Main title="Chat" search={search}>
      <CardList cards={datas} Content={ChatCard} />
    </Main>
  )
}
