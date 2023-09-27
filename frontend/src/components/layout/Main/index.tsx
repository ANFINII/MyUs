import { Search } from 'types/internal/media'

interface Props {
  title?: string
  search?: Search
  type?: 'defalt' | 'table'
  children: React.ReactNode
}

export default function Main(props: Props) {
  const { title, search, type = 'defalt', children } = props

  return (
    <main className="main">
      {type === 'defalt' && (
        <>
          {title && <h1>{title}</h1>}
          {search && (
            <section className="search_message">
              「{search.name}」の検索結果「{search.count}」件
            </section>
          )}
          {children}
        </>
      )}
      {type === 'table' && (
        <article className="article_table">
          {title && <h1>{title}</h1>}
          {children}
        </article>
      )}
    </main>
  )
}
