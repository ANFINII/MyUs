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
        <div className="media_detail_grid">
          <MediaDetailCommon title={title} content={content} read={read} created={created} author={author} />
          <div className="ml_20">
            {/* <MediaDetailSide href={`/media/blog/${id}`} imageUrl="" nickname="" /> */}
            {/* {% include 'media/blog/blog_article_detail.html' %} */}
          </div>
        </div>
      </MediaDetail>
    </Main>
  )
}
