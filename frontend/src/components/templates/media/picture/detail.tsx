import { PictureDetailOut } from 'types/internal/media/detail'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import MediaDetail from 'components/widgets/Media/Detail'
import MediaDetailCommon from 'components/widgets/Media/Detail/Common'
import style from './Detail.module.scss'

interface Props {
  data: PictureDetailOut
}

export default function PictureDetail(props: Props): React.JSX.Element {
  const { data } = props
  const { detail, list } = data
  const { image, publish, ...other } = detail

  const { toast, handleToast } = useToast()

  return (
    <Main metaTitle="Picture" toast={toast}>
      <MediaDetail publish={publish}>
        <div className={style.media_detail_picture}>
          <div className={style.media_detail_contents}>
            <img src={image} alt={other.title} />
          </div>
        </div>
        <Divide />
        <MediaDetailCommon media={{ type: 'picture', ...other }} list={list} handleToast={handleToast} />
      </MediaDetail>
    </Main>
  )
}
