import { Search } from 'types/internal/media'
import { ToastType, MetaType } from 'types/internal/other'
import Footer from 'components/layout//Footer'
import Meta from 'components/layout/Head/Meta'
import Toast from 'components/parts/Toast'

interface Props {
  title?: string
  isTitle?: boolean
  search?: Search
  toast?: ToastType
  type?: 'defalt' | 'table'
  meta?: MetaType
  children: React.ReactNode
}

export default function Main(props: Props) {
  const { title, isTitle = true, search, toast, type = 'defalt', meta, children } = props

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
      <Toast {...toast} />
    </main>
  )
}
