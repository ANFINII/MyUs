import { Search } from 'types/internal/media'
import { ToastType, MetaType } from 'types/internal/other'
import Footer from 'components/layout//Footer'
import Meta from 'components/layout/Head/Meta'
import Toast from 'components/parts/Toast'

interface Props {
  title?: string
  metaTitle?: string
  isTitle?: boolean
  search?: Search
  toast?: ToastType
  type?: 'defalt' | 'table'
  meta?: MetaType
  children: React.ReactNode
}

export default function Main(props: Props) {
  const { title, metaTitle, isTitle = true, search, toast, type = 'defalt', meta, children } = props

  return (
    <main className="main">
      <Meta title={title || metaTitle} {...meta} />
      {type === 'defalt' && (
        <>
          {isTitle && !metaTitle && <h1 className="main_title">{title}</h1>}
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
          {title && !metaTitle && <h1 className="main_title">{title}</h1>}
          {children}
          <Footer />
        </article>
      )}
      <Toast {...toast} />
    </main>
  )
}
