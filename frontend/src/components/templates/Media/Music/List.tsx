import { Query, MusicResponse } from 'types/media'
import Main from 'components/layout/Main'
import ArticleMusic from 'components/wigets/Article/Music'

interface Props {
  query?: Query
  datas: MusicResponse[]
}

export default function MusicList(props: Props) {
  const { query, datas } = props

  return (
    <Main title="MyUsミュージック" hero="Music" query={query}>
      <article className="article_list">
        {datas.map((data) => (
          <ArticleMusic data={data} key={data.id} />
        ))}
      </article>
    </Main>
  )
}
