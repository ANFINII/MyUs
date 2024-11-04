import ExImage from 'components/parts/ExImage'
// import MediaContent from 'components/widgets/Common/MediaContent'
// import ContentTitle from 'components/widgets/Common/MediaContent'

interface Props {
  href: string
  title: string
  imageUrl: string
  nickname: string
  read: number
  totalLike: number
  created: string
}

export default function MediaDetailSide(props: Props) {
  // const { href, title, imageUrl, nickname, read, totalLike, created } = props
  const { href, imageUrl } = props

  return (
    <section className="section_detail">
      <div className="main_decolation">
        <a href={href} className="content_side">
          <figure className="content_size">
            <ExImage src={imageUrl} className="radius_8" />
          </figure>
          {/* <div className="author_space_side">
            <ContentTitle title={title} nickname={nickname} read={read} totalLike={totalLike} created={created} />
          </div> */}
        </a>
      </div>
    </section>
  )
}
