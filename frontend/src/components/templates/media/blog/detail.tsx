import { useTranslation } from 'react-i18next'
import { BlogDetailOut } from 'types/internal/media/output'
import { MediaPath } from 'utils/constants/enum'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Alert from 'components/parts/Alert'
import Divide from 'components/parts/Divide'
import FormatHtml from 'components/parts/FormatHtml'
import MediaDetail from 'components/widgets/Media/Detail'
import MediaDetailCommon from 'components/widgets/Media/Detail/Common'
import style from './Detail.module.scss'

interface Props {
  data: BlogDetailOut
}

export default function BlogDetail(props: Props): React.JSX.Element {
  const { data } = props
  const { detail, list } = data
  const { publish, richtext, isPromotion, ...other } = detail

  const { t } = useTranslation()
  const { toast, handleToast } = useToast()

  return (
    <Main metaTitle="Blog" toast={toast}>
      <MediaDetail publish={publish}>
        <div className={style.media_detail}>
          {isPromotion && <Alert type="info">{t('media.blog.promotion')}</Alert>}
          <FormatHtml content={richtext} isSponsored={isPromotion} />
        </div>
        <Divide />
        <MediaDetailCommon media={{ mediaPath: MediaPath.Blog, ...other }} list={list} handleToast={handleToast} />
      </MediaDetail>
    </Main>
  )
}
