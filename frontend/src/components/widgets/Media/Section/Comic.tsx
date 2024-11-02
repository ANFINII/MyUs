import Link from 'next/link'
import { Comic } from 'types/internal/media'
import ExImage from 'components/parts/ExImage'
import AuthorLink from 'components/parts/AuthorLink'
import ContentTitle from 'components/widgets/Common/ContentTitle'
import style from './Section.module.scss'

interface Props {
  data: Comic
}

export default function SectionComic(props: Props) {
  const { data } = props
  const { author, id, title, image, read, like, created } = data
  const { nickname } = author

  return (
    <section className={style.section_list}>
      <div className={style.decolation}>
        <Link href={`/media/comic/${id}`}>
          <ExImage src={image} width="272" height="153" className="radius_8" />
          <div className={style.author_space}>
            <AuthorLink imageUrl={author.avatar} nickname={nickname} />
            <ContentTitle title={title} nickname={nickname} read={read} totalLike={like} created={created} />
          </div>
        </Link>
      </div>
    </section>
  )
}
