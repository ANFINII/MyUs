import { useTranslation } from 'react-i18next'
import { Blog } from 'types/internal/media/output'
import Card from 'components/parts/Card'
import ExImage from 'components/parts/ExImage'
import Link from 'components/parts/Link'
import style from './Blog.module.scss'
import CardMediaContent from '../Content'

interface Props {
  item: Blog
}

export default function BlogCard(props: Props): React.JSX.Element {
  const { item } = props
  const { ulid, image, isPromotion } = item

  const { t } = useTranslation()

  return (
    <Card className={style.card}>
      <div className={style.thumbnail_wrap}>
        <Link href={`/media/blog/${ulid}`}>
          <ExImage src={image} width="312" height="195" className={style.thumbnail} />
        </Link>
        {isPromotion && <span className={style.promotion}>{t('media.blog.promotionBadge')}</span>}
      </div>
      <CardMediaContent href={`/media/blog/${ulid}`} media={item} />
    </Card>
  )
}
