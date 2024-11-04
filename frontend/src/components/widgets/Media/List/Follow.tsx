import style from './MediaList.module.scss'

interface ObjectName {
  nickname: string
}

interface Props<T extends ObjectName> {
  datas: T[]
  MediaMedia: React.ComponentType<{ data: T }>
}

export default function FollowList<T extends ObjectName>(props: Props<T>) {
  const { datas, MediaMedia } = props

  return (
    <article className={style.media_list}>
      {datas.map((data) => (
        <MediaMedia key={data.nickname} data={data} />
      ))}
    </article>
  )
}
