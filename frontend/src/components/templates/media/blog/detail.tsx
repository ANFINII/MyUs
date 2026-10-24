import { BlogDetailOut } from 'types/internal/media/output'
import { MediaPath } from 'utils/constants/enum'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import BlogArticle from 'components/widgets/BlogArticle'
import MediaDetail from 'components/widgets/Media/Detail'
import MediaDetailCommon from 'components/widgets/Media/Detail/Common'

interface Props {
  data: BlogDetailOut
}

export default function BlogDetail(props: Props): React.JSX.Element {
  const { data } = props
  const { detail, list } = data
  const { publish, richtext, isPromotion, ...other } = detail

  const { toast, handleToast } = useToast()

  return (
    <Main metaTitle="Blog" toast={toast}>
      <MediaDetail publish={publish}>
        <BlogArticle richtext={richtext} isPromotion={isPromotion} />
        <Divide />
        <MediaDetailCommon media={{ mediaPath: MediaPath.Blog, ...other }} list={list} handleToast={handleToast} />
      </MediaDetail>
    </Main>
  )
}
