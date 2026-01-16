import { BlogDetailOut } from 'types/internal/media/detail'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import FormatHtml from 'components/parts/FormatHtml'
import MediaDetail from 'components/widgets/Media/Detail'
import MediaDetailCommon from 'components/widgets/Media/Detail/Common'

interface Props {
  data: BlogDetailOut
}

export default function BlogDetail(props: Props): React.JSX.Element {
  const { data } = props
  const { detail, list } = data
  const { publish, richtext, ...other } = detail

  const { toast, handleToast } = useToast()

  return (
    <Main metaTitle="Blog" toast={toast}>
      <MediaDetail publish={publish}>
        <div className="media_detail_blog quill_content">
          <FormatHtml content={richtext} />
        </div>
        <Divide />
        <MediaDetailCommon media={{ type: 'blog', ...other }} list={list} handleToast={handleToast} />
      </MediaDetail>
    </Main>
  )
}
