interface Props {
  publish: boolean
  children: React.ReactNode
}

export default function MediaDetail(props: Props): React.JSX.Element {
  const { publish, children } = props

  return (
    <article>
      {publish ? <>{children}</> : <h2 className="unpublished">非公開に設定されてます!</h2>}
    </article>
  )
}
