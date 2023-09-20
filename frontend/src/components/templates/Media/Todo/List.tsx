import { Search, MediaResponse } from 'types/media'
import Main from 'components/layout/Main'
import ArticleTodo from 'components/widgets/Article/Todo'

interface Props {
  search?: Search
  datas: MediaResponse[]
}

export default function Todos(props: Props) {
  const { search, datas } = props

  return (
    <Main title="Todo" search={search}>
      <article className="article_list">
        {datas.map((data) => (
          <ArticleTodo data={data} key={data.id} />
        ))}
      </article>
    </Main>
  )
}
