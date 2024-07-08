import { Search } from 'types/internal/media'
import Footer from 'components/layout//Footer'
import Meta from 'components/layout/Head/Meta'

interface Props {
  title?: string
  isTitle?: boolean
  search?: Search
  type?: 'defalt' | 'table'
  meta?: {
    description?: string
    url?: string
    locale?: string
    siteName?: string
    canonical?: string
  }
  children: React.ReactNode
}

export default function Main(props: Props) {
  const { title, isTitle = true, search, type = 'defalt', meta, children } = props

  return (
    <main className="main">
      <Meta title={title} {...meta} />
      {type === 'defalt' && (
        <>
          {isTitle && <h1 className="main_title">{title}</h1>}
          {search?.name && (
            <section className="search_message">
              「{search.name}」の検索結果「{search.count}」件
            </section>
          )}
          {children}
        </>
      )}
      {type === 'table' && (
        <article className="article_table">
          {title && <h1 className="main_title">{title}</h1>}
          {children}
          <Footer />
        </article>
      )}
    </main>
  )
}
