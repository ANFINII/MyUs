import style from './CardList.module.scss'

interface ObjectId {
  ulid: string
}

interface Props<T extends ObjectId> {
  cards: T[]
  Content: React.ComponentType<{ data: T }>
}

export default function CardList<T extends ObjectId>(props: Props<T>) {
  const { cards, Content } = props

  return (
    <article className={style.card_list}>
      {cards.map((card) => (
        <Content key={card.ulid} data={card} />
      ))}
    </article>
  )
}
