import { Picture } from 'types/internal/media'
import Main from 'components/layout/Main'

interface Props {
  datas: Picture
}

export default function BlogDetail(props: Props) {
  const { datas } = props

  return (
    <Main title="Blog">
      <article className="article_list">BlogDetail</article>
    </Main>
  )
}
