import Link from 'next/link'
import { Picture } from 'types/internal/media'
import ExImage from 'components/parts/ExImage'
import AuthorSpace from 'components/widgets/Common/AuthorSpace'
import ContentTitle from 'components/widgets/Common/ContentTitle'

interface Props {
  data: Picture
}

export default function ArticlePicture(props: Props) {
  const { data } = props
  const { author, id, title, image, read, like, created } = data
  const { nickname } = author

  return (
    <section className="section_list">
      <div className="main_decolation">
        <Link href={`/media/picture/${id}`}>
          <figure>
            <ExImage src={image} width="272" height="153" className="radius_8" />
          </figure>
          <div className="author_space">
            <AuthorSpace imageUrl={author.image} nickname={nickname} />
            <ContentTitle title={title} nickname={nickname} read={read} totalLike={like} created={created} />
          </div>
        </Link>
      </div>
    </section>
  )
}
