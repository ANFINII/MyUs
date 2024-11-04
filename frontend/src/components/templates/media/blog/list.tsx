import { Blog } from 'types/internal/media'
import { getBlogs } from 'api/internal/media/list'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import MediaList from 'components/widgets/Media/List/Media'
import MediaBlog from 'components/widgets/Media/Index/Blog'

interface Props {
  datas: Blog[]
}

export default function Blogs(props: Props) {
  const { datas } = props

  const { search, newDatas } = useNewDatas<Blog[]>({ datas, getDatas: (search) => getBlogs(search) })

  return (
    <Main title="Blog" search={{ name: search, count: newDatas.length }}>
      <MediaList datas={newDatas} MediaMedia={MediaBlog} />
    </Main>
  )
}
