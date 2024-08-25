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
  buttonArea?: React.ReactNode
  children: React.ReactNode
}

export default function Main(props: Props) {
  const { title, metaTitle, meta, search, toast, type = 'defalt', buttonArea, children } = props

  const { user } = useUser()

  return (
    <main className="main">
      <Meta title={title || metaTitle} {...meta} />
      {type === 'defalt' && (
        <>
          <div>
            {title && <h1 className="main_title">{title}</h1>}
            {search?.name && (
              <section className="search_message">
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
            {buttonArea && user.isActive && <div className="main_button_area">{buttonArea}</div>}
          </div>
          <article className="main_article">{children}</article>
          <Footer />
        </>
      )}
      <Toast {...toast} />
    </main>
  )
}
