import { getBlogs } from 'api/internal/media/list'
import { Blog } from 'types/internal/media'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import ArticleBlog from 'components/widgets/Article/Blog'

interface Props {
  datas: Blog[]
}

export default function Blogs(props: Props) {
  const { datas } = props

  const { search, newDatas } = useNewDatas<Blog[]>({ datas, getDatas: (search) => getBlogs(search) })

  return (
    <Main title="Blog" search={{ name: search, count: newDatas.length }}>
      <article className="article_list">
        {newDatas.map((data) => (
          <ArticleBlog key={data.id} data={data} />
        ))}
      </article>
    </Main>
  )
}
