import { lazy, Suspense, useRef } from 'react'
import Player from 'video.js/dist/types/player'
import { Video } from 'types/internal/media/output'
import { useRouter } from 'components/hooks/useRouter'
import Card from 'components/parts/Card'
import ExImage from 'components/parts/ExImage'
import style from './Video.module.scss'
import CardMediaContent from '../Content'

const VideoJS = lazy(() => import('components/widgets/Video/videojs'))

interface Props {
  item: Video
}

export default function VideoCard(props: Props): React.JSX.Element {
  const { item } = props
  const { ulid, image, convert } = item

  const router = useRouter()
  const playerRef = useRef<Player | null>(null)

  const handleClick = () => router.push(`/media/video/${ulid}`)

  const handleMouseEnter = () => {
    const player = playerRef.current
    if (player?.play) {
      player.play()?.catch(() => {
        // 再生失敗を静かに処理
      })
    }
  }

  const handleMouseLeave = () => {
    const player = playerRef.current
    if (player) {
      player.pause?.()
      player.currentTime?.(0)
      player.hasStarted?.(false)
    }
  }

  const handlePlayerReady = (player: Player) => {
    playerRef.current = player
    if (player?.muted) {
      player.muted(true)
    }
  }

  return (
    <Card className={style.card}>
      <div className="video video_auto" onClick={handleClick} onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
        <Suspense fallback={<ExImage src={image} width="312" height="195" />}>
          <VideoJS
            onReady={handlePlayerReady}
            options={{
              src: convert,
              poster: image,
              width: 312,
              height: 195,
              muted: true,
              controls: false,
              autoplay: false,
              loop: true,
              preload: 'metadata',
            }}
          />
        </Suspense>
      </div>
      <CardMediaContent href={`/media/video/${ulid}`} media={item} />
    </Card>
  )
}
