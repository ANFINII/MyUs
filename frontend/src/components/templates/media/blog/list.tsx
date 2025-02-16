import { Blog } from 'types/internal/media'
import { getBlogs } from 'api/internal/media/list'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import MediaBlog from 'components/widgets/Media/Index/Blog'
import MediaList from 'components/widgets/Media/List/Media'

interface Props {
  datas: Blog[]
}

export default function Blogs(props: Props): JSX.Element {
  const { datas } = props

  const { search, newDatas } = useNewDatas<Blog[]>({ datas, getDatas: (search) => getBlogs({ search }) })

  return (
    <Main title="Blog" search={{ name: search, count: newDatas.length }}>
      <MediaList medias={newDatas} MediaComponent={MediaBlog} />
    </Main>
  )
}
