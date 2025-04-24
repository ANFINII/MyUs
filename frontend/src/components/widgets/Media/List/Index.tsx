import style from './MediaList.module.scss'

interface Props {
  title: string
  children: React.ReactNode
}

export default function MediaIndex(props: Props): JSX.Element {
  const { title, children } = props

  return (
    <article className={style.media_index}>
      <h2>{title}</h2>
      {children}
    </article>
  )
}
