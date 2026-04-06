import { Blog } from 'types/internal/media'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import CardList from 'components/widgets/Card/List'
import MediaBlog from 'components/widgets/Media/Index/Blog'

interface Props {
  datas: Blog[]
}

export default function Blogs(props: Props): React.JSX.Element {
  const { datas } = props

  const search = useSearch(datas)

  return (
    <Main title="Blog" search={search}>
      <CardList cards={datas} Content={MediaBlog} />
    </Main>
  )
}
