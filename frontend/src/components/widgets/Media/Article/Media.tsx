import style from './Article.module.scss'

interface ObjectId {
  id: number
}

interface Props<T extends ObjectId> {
  datas: T[]
  SectionMedia: React.ComponentType<{ data: T }>
}

export default function ArticleMedia<T extends ObjectId>(props: Props<T>) {
  const { datas, SectionMedia } = props

  return (
    <article className={style.article_list}>
      {datas.map((data) => (
        <SectionMedia key={data.id} data={data} />
      ))}
    </article>
  )
}
