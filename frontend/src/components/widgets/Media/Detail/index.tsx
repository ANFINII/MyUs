import style from './Common.module.scss'

interface Props {
  publish: boolean
  children: React.ReactNode
}

export default function MediaDetail(props: Props): React.JSX.Element {
  const { publish, children } = props

  return (
    <article>
      {publish ? <>{children}</> : <h2 className={style.unpublished}>非公開に設定されてます!</h2>}
    </article>
  )
}
