import Divide from 'components/parts/Divide'
import style from './Article.module.scss'

interface Props {
  title: string
  divide?: boolean
  children: React.ReactNode
}

export default function ArticleIndex(props: Props) {
  const { title, divide = true, children } = props

  return (
    <>
      <article className={style.article_index}>
        <h2>{title}</h2>
        {children}
      </article>
      {divide && <Divide />}
    </>
  )
}
