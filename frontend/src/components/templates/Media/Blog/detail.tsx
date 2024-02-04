import { Blog } from 'types/internal/media'
import Main from 'components/layout/Main'
import MediaDetail from 'components/widgets/MediaDetail'
import MediaDetailCommon from 'components/widgets/MediaDetail/Common'
import MediaDetailInfo from 'components/widgets/MediaDetail/Info'

interface Props {
  data: Blog
}

export default function BlogDetail(props: Props) {
  const { data } = props
  const { publish } = data

  return (
    <Main title="Blog" isTitle={false}>
      <MediaDetail publish={publish}>
        <div className="article_detail_blog quill_content">{/* <p>{{ object.richtext|safe }}</p> */}</div>
        <hr />
        <div className="article_detail_section">
          <div className="article_detail_section_1">
            <MediaDetailCommon data={data} />
          </div>
          <div className="article_detail_section_2">
            <MediaDetailInfo />
            {/* {% include 'media/blog/blog_article_detail.html' %} */}
          </div>
        </div>

        {/* <div className="article_detail_blog quill_content">
          <></>
        </div>
        <hr />
        <div className="article_detail_section">
          <div className="article_detail_section_1">
            <></>
          </div>
          <div className="article_detail_section_2">
            <MediaDetailInfo />
          </div>
        </div> */}
      </MediaDetail>
    </Main>
  )
}
