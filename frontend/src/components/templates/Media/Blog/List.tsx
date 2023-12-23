import { Search, Picture } from 'types/internal/media'
import Main from 'components/layout/Main'
import ArticleBlog from 'components/widgets/Article/Blog'

interface Props {
  search?: Search
  datas: Picture[]
}

export default function Blogs(props: Props) {
  const { search, datas } = props

  return (
    <Main title="Blog" search={search}>
      <article className="article_list">
        {datas.map((data) => (
          <ArticleBlog data={data} key={data.id} />
        ))}
      </article>
    </Main>
  )
}
