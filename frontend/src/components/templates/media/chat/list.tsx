import { Chat } from 'types/internal/media'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import CardList from 'components/widgets/Card/List'
import MediaChat from 'components/widgets/Media/Index/Chat'

interface Props {
  datas: Chat[]
}

export default function Chats(props: Props): React.JSX.Element {
  const { datas } = props

  const search = useSearch(datas)

  return (
    <Main title="Chat" search={search}>
      <CardList cards={datas} Content={MediaChat} />
    </Main>
  )
}
