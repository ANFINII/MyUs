import { getPictures } from 'api/media/get/list'
import { Picture } from 'types/internal/media'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import ArticlePicture from 'components/widgets/Article/Picture'

interface Props {
  datas: Picture[]
}

export default function Pictures(props: Props) {
  const { datas } = props

  const { search, newDatas } = useNewDatas<Picture[]>({ datas, getDatas: (search) => getPictures(search) })

  return (
    <Main title="Picture" search={{ name: search, count: newDatas.length }}>
      <article className="article_list">
        {newDatas.map((data) => (
          <ArticlePicture key={data.id} data={data} />
        ))}
      </article>
    </Main>
  )
}
