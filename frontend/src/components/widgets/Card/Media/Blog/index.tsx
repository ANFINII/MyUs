import { useTranslation } from 'react-i18next'
import { Blog } from 'types/internal/media/output'
import ImageCard from '../Image'

interface Props {
  item: Blog
}

export default function BlogCard(props: Props): React.JSX.Element {
  const { item } = props
  const { ulid, image, isPromotion } = item

  const { t } = useTranslation()

  return <ImageCard href={`/media/blog/${ulid}`} image={image} media={item} badge={isPromotion ? t('media.blog.promotionBadge') : ''} />
}
