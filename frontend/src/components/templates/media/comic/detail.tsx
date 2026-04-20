import { ComicDetailOut } from 'types/internal/media/output'
import { MediaPath } from 'utils/constants/enum'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import ComicViewer from 'components/widgets/ComicViewer'
import MediaDetail from 'components/widgets/Media/Detail'
import MediaDetailCommon from 'components/widgets/Media/Detail/Common'
interface Props {
  data: ComicDetailOut
}

export default function ComicDetail(props: Props): React.JSX.Element {
  const { data } = props
  const { detail, list } = data
  const { image, pages, publish, ...other } = detail

  const { toast, handleToast } = useToast()

  return (
    <Main metaTitle="Comic" toast={toast}>
      <MediaDetail publish={publish}>
        <ComicViewer pages={[image, ...pages]} />
        <Divide />
        <MediaDetailCommon media={{ mediaPath: MediaPath.Comic, ...other }} list={list} handleToast={handleToast} />
      </MediaDetail>
    </Main>
  )
}
