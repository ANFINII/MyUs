import { Query, MediaResponse } from 'types/media'
import Main from 'components/layout/Main'
import ArticleComic from 'components/widgets/Article/Comic'

interface Props {
  query?: Query
  datas: Array<MediaResponse>
}

export default function ComicList(props: Props) {
  const { query, datas } = props

  return (
    <Main title="MyUsコミック" name="Comic" query={query}>
      <article className="article_list">
        {datas.map((data) => (
          <ArticleComic data={data} key={data.id} />
        ))}
      </article>
    </Main>
  )
}
