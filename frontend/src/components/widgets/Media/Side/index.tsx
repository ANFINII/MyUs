import ExImage from 'components/parts/ExImage'
// import MediaContent from 'components/widgets/Common/MediaContent'
// import ContentTitle from 'components/widgets/Common/MediaContent'
import style from './Side.module.scss'

interface Props {
  href: string
  title: string
  imageUrl: string
  nickname: string
  read: number
  like: number
  created: string
}

export default function MediaDetailSide(props: Props) {
  // const { href, title, imageUrl, nickname, read, like, created } = props
  const { href, imageUrl } = props

  return (
    <section className={style.media_detail_side}>
      <div className="main_decolation">
        <a href={href} className={style.media_content}>
          <figure className="content_size">
            <ExImage src={imageUrl} className="radius_8" />
          </figure>
          {/* <div className="author_space_side">
            <ContentTitle title={title} nickname={nickname} read={read} like={like} created={created} />
          </div> */}
          {/* <div className={style.media_content}>
            <MediaContent href={`/media/music/${id}`} media={media} />
          </div> */}
        </a>
      </div>
    </section>
  )
}
