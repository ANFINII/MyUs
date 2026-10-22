import { Advertise } from 'types/internal/advertise'
import { postAdvertiseRead } from 'api/internal/advertise'
import { isHttpsUrl } from 'utils/functions/validation'
import ExImage from 'components/parts/ExImage'
import IconCaret from 'components/parts/Icon/Caret'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import style from './Advertise.module.scss'

interface Props {
  item: Advertise
}

export default function AdvertiseCard(props: Props): React.JSX.Element {
  const { item } = props
  const { ulid, url, title, image, video, read } = item

  const handleRead = () => postAdvertiseRead(ulid)

  return (
    <article className={style.card}>
      <a href={isHttpsUrl(url) ? url : undefined} target="_blank" rel="noopener noreferrer" className={style.link} onClick={handleRead}>
        <HStack gap="4">
          {video ? (
            <video src={video} poster={image} width="192" height="108" preload="metadata" muted className={style.thumbnail} />
          ) : (
            <ExImage src={image} width="192" height="108" className={style.thumbnail} />
          )}
          <VStack gap="2" className={style.content}>
            <div title={title} className={style.title}>
              {title}
            </div>
            <div className={style.font}>
              <IconCaret size="14" className={style.margin} />
              {read}
            </div>
          </VStack>
        </HStack>
      </a>
    </article>
  )
}
