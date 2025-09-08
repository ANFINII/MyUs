import { Blog } from 'types/internal/media'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import MediaBlog from 'components/widgets/Media/Index/Blog'
import MediaList from 'components/widgets/Media/List/Media'

interface Props {
  datas: Blog[]
}

export default function Blogs(props: Props): React.JSX.Element {
  const { datas } = props

  const search = useSearch(datas)

  return (
    <Main title="Blog" search={search}>
      <MediaList medias={datas} MediaComponent={MediaBlog} />
    </Main>
  )
}
