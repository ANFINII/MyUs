import { Query } from 'types/media'
import Meta from 'components/layout/Head/Meta'

interface Props {
  title?: string
  name?: string
  query?: Query
  children: React.ReactNode
}

export default function Main(props: Props) {
  const { title, name, query, children } = props

  return (
    <>
      <Meta title={title} />
      <main className="main">
        {name && <h1>{name}</h1>}
        {query && (
          <section className="search_message">
            「{query.name}」の検索結果「{query.count}」件
          </section>
        )}
        {children}
      </main>
    </>
  )
}
