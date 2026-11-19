import { useTranslation } from 'react-i18next'
import { ComicDetailOut } from 'types/internal/media/output'
import { MediaPath } from 'utils/constants/enum'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import ComicViewer from 'components/widgets/ComicViewer'
import MediaDetail from 'components/widgets/Media/Detail'
import MediaDetailCommon from 'components/widgets/Media/Detail/Common'
import Paywall from 'components/widgets/Paywall'

interface Props {
  data: ComicDetailOut
}

export default function ComicDetail(props: Props): React.JSX.Element {
  const { data } = props
  const { detail, list, series } = data
  const { image, pageCount, isPurchased, pages, product, publish, ...other } = detail

  const { t } = useTranslation()
  const { toast, handleToast } = useToast()

  const isLocked = product !== null && pages.length < pageCount && !isPurchased

  return (
    <Main metaTitle="Comic" toast={toast}>
      <MediaDetail publish={publish}>
        <ComicViewer pages={[image, ...pages]} />
        {isLocked && product !== null && <Paywall title={t('media.comic.paywallTitle')} notice={t('media.comic.paywallNotice')} product={product} handleToast={handleToast} />}
        <Divide />
        <MediaDetailCommon media={{ mediaPath: MediaPath.Comic, ...other }} list={list} series={series} handleToast={handleToast} />
      </MediaDetail>
    </Main>
  )
}
