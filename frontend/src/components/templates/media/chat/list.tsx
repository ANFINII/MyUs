import { Chat } from 'types/internal/media'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import MediaChat from 'components/widgets/Media/Index/Chat'
import MediaList from 'components/widgets/Media/List/Media'

interface Props {
  datas: Chat[]
}

export default function Chats(props: Props): React.JSX.Element {
  const { datas } = props

  const search = useSearch(datas)

  return (
    <Main title="Chat" search={search}>
      <MediaList medias={datas} MediaComponent={MediaChat} />
    </Main>
  )
}
