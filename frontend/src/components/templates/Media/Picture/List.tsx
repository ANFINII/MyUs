import { Search, Picture } from 'types/internal/media'
import Layout from 'components/layout'
import ArticlePicture from 'components/widgets/Article/Picture'

interface Props {
  search?: Search
  datas: Picture[]
}

export default function Pictures(props: Props) {
  const { search, datas } = props

  return (
    <Layout title="Picture" search={search}>
      <article className="article_list">
        {datas.map((data) => (
          <ArticlePicture data={data} key={data.id} />
        ))}
      </article>
    </Layout>
  )
}
