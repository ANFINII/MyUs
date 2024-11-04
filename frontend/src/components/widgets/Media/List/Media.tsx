import style from './MediaList.module.scss'

interface ObjectId {
  id: number
}

interface Props<T extends ObjectId> {
  medias: T[]
  MediaComponent: React.ComponentType<{ media: T }>
}

export default function MediaList<T extends ObjectId>(props: Props<T>) {
  const { medias, MediaComponent } = props

  return (
    <article className={style.media_list}>
      {medias.map((media) => (
        <MediaComponent key={media.id} media={media} />
      ))}
    </article>
  )
}
