import {Query, MediaResponse} from 'utils/type'
import Main from 'components/layouts/Main'
import ArticleComic from 'components/wigets/Article/Comic'

interface Props {
  query?: Query
  datas: Array<MediaResponse>
}

export default function ComicList(props: Props) {
  const {query, datas} = props
  return (
    <Main title="MyUsコミック" hero="Comic" query={query}>
      <article className="article_list">
        {datas.map((data) => (
          <ArticleComic data={data} key={data.id} />
        ))}
      </article>
    </Main>
  )
}
