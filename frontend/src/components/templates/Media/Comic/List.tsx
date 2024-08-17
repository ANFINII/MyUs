import { getComics } from 'api/internal/media/list'
import { Comic } from 'types/internal/media'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import ArticleComic from 'components/widgets/Article/Comic'

interface Props {
  datas: Comic[]
}

export default function Comics(props: Props) {
  const { datas } = props

  const { search, newDatas } = useNewDatas<Comic[]>({ datas, getDatas: (search) => getComics(search) })

  return (
    <Main title="Comic" search={{ name: search, count: newDatas.length }}>
      <article className="article_list">
        {newDatas.map((data) => (
          <ArticleComic data={data} key={data.id} />
        ))}
      </article>
    </Main>
  )
}
