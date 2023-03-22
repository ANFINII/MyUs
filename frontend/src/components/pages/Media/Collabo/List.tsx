import {Query, MediaResponse} from 'utils/type'
import Main from 'components/layouts/Main'
import ArticleCollabo from 'components/elements/Article/Collabo'

interface Props {
  query?: Query
  datas: Array<MediaResponse>
}

export default function CollaboList(props: Props) {
  const {query, datas} = props
  return (
    <Main title="MyUsコラボ" hero="Collabo" query={query}>
      <ArticleCollabo datas={datas} />
    </Main>
  )
}
