import Link from 'next/link'
import Image from 'next/image'
import config from 'api/config'
import {ImageResponse} from 'utils/type'
import AuthorSpace from 'components/elements/Common/AuthorSpace'
import ContentTitle from 'components/elements/Common/ContentTitle'

interface Props {datas: Array<ImageResponse>}

export default function ArticlePicture(props: Props) {
  const {datas} = props
  return (
    <article className="article_list">
      {datas.map((data) => {
        const pictureUrl = config.baseUrl + data.image
        const imageUrl = config.baseUrl + data.author.image
        const nickname = data.author.nickname
        return (
          <section className="section_list" key={data.id}>
            <figure className="main_decolation">
              <Link href="/picture/detail/[id][title]">
                <Image src={pictureUrl} width={272} height={153} alt="" />
              </Link>
              <Link href="/picture/detail/[id][title]" className="author_space">
                <AuthorSpace imageUrl={imageUrl} nickname={nickname} />
                <ContentTitle title={data.title} nickname={nickname} read={data.read} totalLike={data.like} created={data.created} />
              </Link>
            </figure>
          </section>
        )
      })}
    </article>
  )
}
