import { Search, MusicResponse } from 'types/media'
import Main from 'components/layout/Main'
import ArticleMusic from 'components/widgets/Article/Music'

interface Props {
  search?: Search
  datas: MusicResponse[]
}

export default function Musics(props: Props) {
  const { search, datas } = props

  return (
    <Main title="Music" search={search}>
      <article className="article_list">
        {datas.map((data) => (
          <ArticleMusic data={data} key={data.id} />
        ))}
      </article>
    </Main>
  )
}
