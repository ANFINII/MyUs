import { Comic } from 'types/internal/media'
import { getComics } from 'api/internal/media/list'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import ArticleMedia from 'components/widgets/Media/Article/Media'
import SectionComic from 'components/widgets/Media/Section/Comic'

interface Props {
  datas: Comic[]
}

export default function Comics(props: Props) {
  const { datas } = props

  const { search, newDatas } = useNewDatas<Comic[]>({ datas, getDatas: (search) => getComics(search) })

  return (
    <Main title="Comic" search={{ name: search, count: newDatas.length }}>
      <ArticleMedia datas={newDatas} SectionMedia={SectionComic} />
    </Main>
  )
}
