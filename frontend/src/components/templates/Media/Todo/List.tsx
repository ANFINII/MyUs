import {Query, MediaResponse} from 'types/media'
import Main from 'components/layout/Main'
import ArticleTodo from 'components/widgets/Article/Todo'

interface Props {
  query?: Query
  datas: MediaResponse[]
}

export default function TodoList(props: Props) {
  const {query, datas} = props
  return (
    <Main title="MyUs Todo" hero="Todo" query={query}>
      <article className="article_list">
        {datas.map((data) => (
          <ArticleTodo data={data} key={data.id} />
        ))}
      </article>
    </Main>
  )
}
