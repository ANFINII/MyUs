import Divide from 'components/parts/Divide'

interface Props {
  title: string
  divide?: boolean
  children: React.ReactNode
}

export default function ArticleIndex(props: Props) {
  const { title, divide = true, children } = props

  return (
    <>
      <article className="article_index">
        <h2>{title}</h2>
        {children}
      </article>
      {divide && <Divide />}
    </>
  )
}
