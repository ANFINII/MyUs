import style from './Article.module.scss'

interface ObjectId {
  id: number
}

interface ArticleProps<T extends ObjectId> {
  datas: T[]
  SectionMedia: React.ComponentType<{ data: T }>
}

export default function ArticleList<T extends ObjectId>(props: ArticleProps<T>) {
  const { datas, SectionMedia } = props

  return (
    <article className={style.article_list}>
      {datas.map((data) => (
        <SectionMedia key={data.id} data={data} />
      ))}
    </article>
  )
}
