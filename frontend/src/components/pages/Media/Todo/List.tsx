import {Query, MediaResponse} from 'utils/type'
import Main from 'components/layouts/Main'
import ArticleTodo from 'components/elements/Article/Todo'

interface Props {
  query?: Query
  datas: Array<MediaResponse>
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
