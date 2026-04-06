import style from './CardList.module.scss'

interface ObjectId {
  ulid: string
}

interface Props<T extends ObjectId> {
  items: T[]
  Content: React.ComponentType<{ item: T }>
}

export default function CardList<T extends ObjectId>(props: Props<T>) {
  const { items, Content } = props

  return (
    <article className={style.card_list}>
      {items.map((item) => (
        <Content key={item.ulid} item={item} />
      ))}
    </article>
  )
}
