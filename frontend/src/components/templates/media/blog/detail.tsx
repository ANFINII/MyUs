import { BlogDetailOut } from 'types/internal/media'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import FormatHtml from 'components/parts/FormatHtml'
import Vertical from 'components/parts/Stack/Vertical'
import MediaDetail from 'components/widgets/Media/Detail'
import MediaDetailCommon from 'components/widgets/Media/Detail/Common'
import MediaSideBlog from 'components/widgets/Media/Side'

interface Props {
  data: BlogDetailOut
}

export default function BlogDetail(props: Props): JSX.Element {
  const { data } = props
  const { detail, list } = data
  const { title, content, richtext, read, like, commentCount, publish, created, author, user } = detail

  const { toast, handleToast } = useToast()

  return (
    <Main metaTitle="Blog" toast={toast}>
      <MediaDetail publish={publish}>
        <div className="media_detail_blog quill_content">
          <FormatHtml content={richtext} />
        </div>
        <Divide />
        <div className="media_detail_grid">
          <MediaDetailCommon media={{ title, content, read, like, commentCount, created, author, user, type: 'blog' }} handleToast={handleToast} />
          <div className="ml_20">
            <Vertical gap="4">
              {list.map((media) => (<MediaSideBlog key={media.id} media={media} />))}
            </Vertical>
          </div>
        </div>
      </MediaDetail>
    </Main>
  )
}
