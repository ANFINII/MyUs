import Link from 'next/link'
import AuthorSpace from 'components/elements/Common/AuthorSpace'
import ContentTitle from 'components/elements/Common/ContentTitle'

interface Props {
  imageUrl: string
  nickname?: string
}

export default function CollaboArticle(Props: Props) {
  const {imageUrl, nickname} = Props
  return (
    <article className="article_list">
      {/* {% for item in collabo_list %} */}
      <section className="section_other">
        <div className="main_decolation">
          <Link href="/collabo/detail/[id][title]" className="author_space">
            <AuthorSpace imageUrl={imageUrl} nickname={nickname} />
            <ContentTitle />
          </Link>
        </div>
      </section>
      {/* {% endfor %} */}
    </article>
  )
}
