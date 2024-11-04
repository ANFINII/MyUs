import style from './MediaList.module.scss'

interface ObjectName {
  nickname: string
}

interface Props<T extends ObjectName> {
  medias: T[]
  MediaComponent: React.ComponentType<{ media: T }>
}

export default function FollowList<T extends ObjectName>(props: Props<T>) {
  const { medias, MediaComponent } = props

  return (
    <article className={style.media_list}>
      {medias.map((media) => (
        <MediaComponent key={media.nickname} media={media} />
      ))}
    </article>
  )
}
