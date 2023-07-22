import { Query, ImageResponse } from 'types/media'
import Main from 'components/layout/Main'
import ArticlePicture from 'components/widgets/Article/Picture'

interface Props {
  query?: Query
  datas: ImageResponse[]
}

export default function PictureList(props: Props) {
  const { query, datas } = props
  return (
    <Main title="MyUsピクチャー" hero="Picture" query={query}>
      <article className="article_list">
        {datas.map((data) => (
          <ArticlePicture data={data} key={data.id} />
        ))}
      </article>
    </Main>
  )
}
