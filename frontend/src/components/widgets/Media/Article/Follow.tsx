import style from './Article.module.scss'

interface ObjectName {
  nickname: string
}

interface Props<T extends ObjectName> {
  datas: T[]
  SectionMedia: React.ComponentType<{ data: T }>
}

export default function ArticleFollow<T extends ObjectName>(props: Props<T>) {
  const { datas, SectionMedia } = props

  return (
    <article className={style.article_list}>
      {datas.map((data) => (
        <SectionMedia key={data.nickname} data={data} />
      ))}
    </article>
  )
}
