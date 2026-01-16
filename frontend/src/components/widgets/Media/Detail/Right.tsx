import { Video, Blog } from 'types/internal/media'
import Divide from 'components/parts/Divide'
import VStack from 'components/parts/Stack/Vertical'
import style from './Common.module.scss'
import MediaSideImage from '../Side/Image'

interface Props {
  list: Video[] | Blog[]
}

export default function MediaDetailRight(props: Props): React.JSX.Element {
  const { list } = props

  return (
    <div className={style.media_detail_right}>
      <div className={style.advertise}>
        <h2>広告表示</h2>
        <article className="article_list">{/* {% include 'parts/advertise_article_auto.html' %} */}</article>
      </div>
      <Divide />
      <VStack gap="4">
        {list.map((media) => (
          <MediaSideImage key={media.ulid} href={`/media/blog/${media.ulid}`} src={media.image} media={media} />
        ))}
      </VStack>
    </div>
  )
}
