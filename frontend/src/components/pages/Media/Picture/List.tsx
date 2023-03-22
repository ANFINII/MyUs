import {Query, ImageResponse} from 'utils/type'
import Main from 'components/layouts/Main'
import ArticlePicture from 'components/elements/Article/Picture'

interface Props {
  query?: Query
  datas: Array<ImageResponse>
}

export default function PictureList(props: Props) {
  const {query, datas} = props
  return (
    <Main title="MyUsピクチャー" hero="Picture" query={query}>
      <ArticlePicture datas={datas} />
    </Main>
  )
}
