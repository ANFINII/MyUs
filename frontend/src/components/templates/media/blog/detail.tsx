import { BlogDetailOut } from 'types/internal/media'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import FormatHtml from 'components/parts/FormatHtml'
import MediaDetail from 'components/widgets/Media/Detail'
import MediaDetailCommon from 'components/widgets/Media/Detail/Common'
import MediaDetailSide from 'components/widgets/Media/Detail/Side'

interface Props {
  data: BlogDetailOut
}

export default function BlogDetail(props: Props) {
  const { data } = props
  const { detail, list } = data
  const { title, content, richtext, read, like, commentCount, publish, created, author, user } = detail

  return (
    <Main metaTitle="Blog">
      <MediaDetail publish={publish}>
        <div className="article_detail_blog quill_content">
          <FormatHtml content={richtext} />
        </div>
        <Divide />
        <div className="article_detail_section">
          <div className="article_detail_section_1">
            <MediaDetailCommon title={title} content={content} read={read} like={like} commentCount={commentCount} created={created} author={author} user={user} />
          </div>
          <div className="article_detail_section_2">
            {list.map((data) => (
              <MediaDetailSide
                key={data.id}
                href={`/media/blog/${data.id}`}
                title={data.title}
                imageUrl={data.image}
                nickname={data.author.nickname}
                read={data.read}
                like={data.like}
                created={created}
              />
            ))}
          </div>
        </div>
      </MediaDetail>
    </Main>
  )
}
