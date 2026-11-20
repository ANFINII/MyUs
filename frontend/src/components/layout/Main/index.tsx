import { useTranslation } from 'react-i18next'
import { Search } from 'types/internal/media/output'
import { ToastType, MetaType } from 'types/internal/other'
import cx from 'utils/functions/cx'
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
  size?: 's' | 'l' | 'xl'
  search?: Search
  toast?: ToastType
  isFooter?: boolean
  button?: React.ReactNode
  children: React.ReactNode
}

export default function Main(props: Props): React.JSX.Element {
  const { title, metaTitle, meta, type = 'defalt', size, search, toast, isFooter = type === 'table', button, children } = props

  const { t } = useTranslation()
  const { user } = useUser()

  const content = size ? <div className={cx(style.content, style[size])}>{children}</div> : children

  return (
    <main className={style.main}>
      <Meta title={title || metaTitle} {...meta} />
      {type === 'defalt' && (
        <>
          <div className={style.header}>
            <div>
              {title && <h1 className={style.title}>{title}</h1>}
              {search?.name && <section className={style.search_message}>{t('search.result', { name: search.name, count: search.count })}</section>}
            </div>
            {button && <div className={style.button}>{button}</div>}
          </div>
          {size ? <div className={cx(style.content, style[size])}>{children}</div> : children}
          {isFooter && <Footer />}
        </>
      )}

      {type === 'table' && (
        <>
          <div className={style.header}>
            {title && <h1 className={style.title}>{title}</h1>}
            {button && user.isActive && <div className={style.button}>{button}</div>}
          </div>
          <article className={style.article}>{content}</article>
          {isFooter && <Footer />}
        </>
      )}
      <Toast {...toast} />
    </main>
  )
}
