import { Todo } from 'types/internal/media'
import Main from 'components/layout/Main'
import MediaDetail from 'components/widgets/Media/Detail'
import MediaDetailCommon from 'components/widgets/Media/Detail/Common'

interface Props {
  data: Todo
}

export default function TodoDetail(props: Props) {
  const { data } = props
  const { title, content, read, created, author } = data

  return (
    <Main metaTitle="Todo">
      <MediaDetail publish={true}>
        <div className="media_detail_blog quill_content">{/* <p>{{ object.richtext|safe }}</p> */}</div>
        <hr />
        <div className="media_detail_section">
          <div className="media_detail_section_1">
            <MediaDetailCommon title={title} content={content} read={read} created={created} author={author} />
          </div>
          <div className="media_detail_section_2">
            {/* <MediaDetailSide href={`/media/blog/${id}`} imageUrl="" nickname="" /> */}
            {/* {% include 'media/blog/blog_media_detail.html' %} */}
          </div>
        </div>
      </MediaDetail>
    </Main>
  )
}
