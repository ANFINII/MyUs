import { Search } from 'types/internal/media'
import { ToastType, MetaType } from 'types/internal/other'
import { useUser } from 'components/hooks/useUser'
import Footer from 'components/layout//Footer'
import Meta from 'components/layout/Head/Meta'
import Toast from 'components/parts/Toast'

interface Props {
  title?: string
  metaTitle?: string
  meta?: MetaType
  search?: Search
  toast?: ToastType
  type?: 'defalt' | 'table'
  button?: React.ReactNode
  children: React.ReactNode
}

export default function Main(props: Props): JSX.Element {
  const { title, metaTitle, meta, search, toast, type = 'defalt', button, children } = props

  const { user } = useUser()

  return (
    <main className="main">
      <Meta title={title || metaTitle} {...meta} />
      {type === 'defalt' && (
        <>
          <div>
            {title && <h1 className="main_title">{title}</h1>}
            {search?.name && (
              <section className="main_search_message">
                「{search.name}」の検索結果「{search.count}」件
              </section>
            )}
          </div>
          {children}
        </>
      )}

      {type === 'table' && (
        <>
          <div className="main_header">
            {title && <h1 className="main_title">{title}</h1>}
            {button && user.isActive && <div className="ml_8">{button}</div>}
          </div>
          <article className="mv_24">{children}</article>
          <Footer />
        </>
      )}
      <Toast {...toast} />
    </main>
  )
}
