import Link from 'next/link'
import { Picture } from 'types/internal/media'
import ExImage from 'components/parts/ExImage'
import AuthorSpace from 'components/widgets/Common/AuthorSpace'
import ContentTitle from 'components/widgets/Common/ContentTitle'
import style from './Section.module.scss'

interface Props {
  data: Picture
}

export default function SectionPicture(props: Props) {
  const { data } = props
  const { author, id, title, image, read, like, created } = data
  const { nickname } = author

  return (
    <section className={style.section_list}>
      <div className={style.decolation}>
        <Link href={`/media/picture/${id}`}>
          <ExImage src={image} width="272" height="153" className={style.section_image} />
          <div className={style.author_space}>
            <AuthorSpace imageUrl={author.avatar} nickname={nickname} />
            <ContentTitle title={title} nickname={nickname} read={read} totalLike={like} created={created} />
          </div>
        </Link>
      </div>
    </section>
  )
}
