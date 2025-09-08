import { useRef } from 'react'
import { useRouter } from 'next/router'
import videojs from 'video.js'
import { Video } from 'types/internal/media'
import MediaContent from 'components/widgets/Media/Content'
import VideoJS from 'components/widgets/Video/videojs'
import style from './Media.module.scss'

type Player = ReturnType<typeof videojs>

interface Props {
  media: Video
}

export default function MediaVideo(props: Props): React.JSX.Element {
  const { media } = props
  const { id, image, convert } = media

  const router = useRouter()
  const playerRef = useRef<Player | null>(null)

  const handleClick = () => router.push(`/media/video/${id}`)

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
    <section className={style.media}>
      <div className="video video_auto" onClick={handleClick} onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
        <VideoJS
          onReady={handlePlayerReady}
          options={{
            src: convert,
            poster: image,
            width: 272,
            height: 153,
            muted: true,
            controls: false,
            autoplay: false,
            loop: true,
            preload: 'metadata',
          }}
        />
        <div className={style.media_content}>
          <MediaContent href={`/media/video/${id}`} media={media} />
        </div>
      </div>
    </section>
  )
}
