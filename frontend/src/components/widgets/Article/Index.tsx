interface Props {
  title: string
  children: React.ReactNode
}

export default function ArticleIndex(props: Props) {
  const { title, children } = props

  return (
    <>
      <article className="article_index">
        <h2>{title}</h2>
        {children}
      </article>
      <hr />
    </>
  )
}
