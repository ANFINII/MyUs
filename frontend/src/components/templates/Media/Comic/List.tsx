import { Search, MediaResponse } from 'types/media'
import Main from 'components/layout/Main'
import ArticleComic from 'components/widgets/Article/Comic'

interface Props {
  search?: Search
  datas: Array<MediaResponse>
}

export default function Comics(props: Props) {
  const { search, datas } = props

  return (
    <Main title="Comic" search={search}>
      <article className="article_list">
        {datas.map((data) => (
          <ArticleComic data={data} key={data.id} />
        ))}
      </article>
    </Main>
  )
}
