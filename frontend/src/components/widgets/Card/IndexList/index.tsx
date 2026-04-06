import style from './CardIndexList.module.scss'

interface Props {
  title: string
  children: React.ReactNode
}

export default function CardIndexList(props: Props): React.JSX.Element {
  const { title, children } = props

  return (
    <article className={style.card_list}>
      <h2>{title}</h2>
      {children}
    </article>
  )
}
