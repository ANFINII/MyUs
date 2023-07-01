import { SearchQuery } from 'types/media'
import Meta from 'components/layout/Head/Meta'

interface Props {
  title?: string
  hero?: string
  query?: SearchQuery
  children: React.ReactNode
}

export default function Main(props: Props) {
  const { title, hero, query, children } = props
  return (
    <>
      <Meta title={title} />
      <main className="main">
        {hero && <h1>{hero}</h1>}
        {query && <section className="search_message">「{query.name}」の検索結果「{query.count}」件</section>}
        {children}
      </main>
    </>
  )
}