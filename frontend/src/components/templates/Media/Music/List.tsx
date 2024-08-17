import { getMusics } from 'api/internal/media/list'
import { Music } from 'types/internal/media'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import ArticleMusic from 'components/widgets/Article/Music'

interface Props {
  datas: Music[]
}

export default function Musics(props: Props) {
  const { datas } = props

  const { search, newDatas } = useNewDatas<Music[]>({ datas, getDatas: (search) => getMusics(search) })

  return (
    <Main title="Music" search={{ name: search, count: newDatas.length }}>
      <article className="article_list">
        {newDatas.map((data) => (
          <ArticleMusic key={data.id} data={data} />
        ))}
      </article>
    </Main>
  )
}
