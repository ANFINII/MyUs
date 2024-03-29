import { Search, Picture } from 'types/internal/media'
import Main from 'components/layout/Main'
import ArticlePicture from 'components/widgets/Article/Picture'

interface Props {
  search?: Search
  datas: Picture[]
}

export default function Pictures(props: Props) {
  const { search, datas } = props

  return (
    <Main title="Picture" search={search}>
      <article className="article_list">
        {datas.map((data) => (
          <ArticlePicture data={data} key={data.id} />
        ))}
      </article>
    </Main>
  )
}
