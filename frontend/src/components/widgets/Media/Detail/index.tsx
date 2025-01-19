import style from './MediaDetail.module.scss'

interface Props {
  publish: boolean
  children: React.ReactNode
}

export default function MediaDetail(props: Props): JSX.Element {
  const { publish, children } = props

  return (
    <article className={style.media_detail}>
      {publish ? <>{children}</> : <h2 className="unpublished">非公開に設定されてます!</h2>}
    </article>
  )
}
