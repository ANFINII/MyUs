import { BlogDetailOut } from 'types/internal/media/detail'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import FormatHtml from 'components/parts/FormatHtml'
import VStack from 'components/parts/Stack/Vertical'
import MediaDetail from 'components/widgets/Media/Detail'
import MediaDetailCommon from 'components/widgets/Media/Detail/Common'
import MediaSideImage from 'components/widgets/Media/Side/Image'

interface Props {
  data: BlogDetailOut
}

export default function BlogDetail(props: Props): JSX.Element {
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
        <div className="media_detail_grid">
          <MediaDetailCommon media={{ type: 'blog', ...other }} handleToast={handleToast} />
          <VStack gap="4" className="ml_20">
            {list.map((media) => (
              <MediaSideImage key={media.id} href={`/media/blog/${media.id}`} src={media.image} media={media} />
            ))}
          </VStack>
        </div>
      </MediaDetail>
    </Main>
  )
}
