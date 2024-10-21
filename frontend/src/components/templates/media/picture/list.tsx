import { getPictures } from 'api/internal/media/list'
import { Picture } from 'types/internal/media'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import ArticleMedia from 'components/widgets/Media/Article/Media'
import SectionPicture from 'components/widgets/Media/Section/Picture'

interface Props {
  datas: Picture[]
}

export default function Pictures(props: Props) {
  const { datas } = props

  const { search, newDatas } = useNewDatas<Picture[]>({ datas, getDatas: (search) => getPictures(search) })

  return (
    <Main title="Picture" search={{ name: search, count: newDatas.length }}>
      <ArticleMedia datas={newDatas} SectionMedia={SectionPicture} />
    </Main>
  )
}
