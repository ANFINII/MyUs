import style from './MediaList.module.scss'

interface ObjectId {
  id: number
}

interface Props<T extends ObjectId> {
  datas: T[]
  MediaMedia: React.ComponentType<{ data: T }>
}

export default function MediaList<T extends ObjectId>(props: Props<T>) {
  const { datas, MediaMedia } = props

  return (
    <article className={style.media_list}>
      {datas.map((data) => (
        <MediaMedia key={data.id} data={data} />
      ))}
    </article>
  )
}
