import { Search } from 'types/internal/media/output'
import { ToastType, MetaType } from 'types/internal/other'
import { useUser } from 'components/hooks/useUser'
import Footer from 'components/layout/Footer'
import Meta from 'components/layout/Head/Meta'
import Toast from 'components/parts/Toast'
import style from './Main.module.scss'

interface Props {
  title?: string
  metaTitle?: string
  meta?: MetaType
  type?: 'defalt' | 'table'
  search?: Search
  toast?: ToastType
  isFooter?: boolean
  button?: React.ReactNode
  children: React.ReactNode
}

export default function Main(props: Props): React.JSX.Element {
  const { title, metaTitle, meta, type = 'defalt', search, toast, isFooter = true, button, children } = props

  const { user } = useUser()

  return (
    <main className={style.main}>
      <Meta title={title || metaTitle} {...meta} />
      {type === 'defalt' && (
        <>
          <div>
            {title && <h1 className={style.title}>{title}</h1>}
            {search?.name && (
              <section className={style.search_message}>
                「{search.name}」の検索結果「{search.count}」件
              </section>
            )}
          </div>
          {children}
        </>
      )}

      {type === 'table' && (
        <>
          <div className={style.header}>
            {title && <h1 className={style.title}>{title}</h1>}
            {button && user.isActive && <div className={style.button}>{button}</div>}
          </div>
          <article className={style.article}>{children}</article>
          {isFooter && <Footer />}
        </>
      )}
      <Toast {...toast} />
    </main>
  )
}
