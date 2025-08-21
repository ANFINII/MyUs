import { useRef, useEffect } from 'react'
import videojs from 'video.js'
import 'video.js/dist/video-js.css'

type Player = ReturnType<typeof videojs>
type PlayerOptions = Parameters<typeof videojs>[1]

interface Props {
  options: PlayerOptions
  onReady?: (player: Player) => void
}

export default function VideoJS(props: Props): JSX.Element {
  const { options, onReady } = props

  const videoRef = useRef<HTMLDivElement>(null)
  const playerRef = useRef<Player | null>(null)

  useEffect(() => {
    // Video.jsプレーヤーが一度だけ初期化されることを確認
    // React 18 Strict ModeのためにVideo.jsプレーヤーはコンポーネントelの内部に必要
    if (!playerRef.current && videoRef.current) {
      const videoElement = document.createElement('video-js')
      videoElement.classList.add('vjs-big-play-centered')
      videoRef.current.appendChild(videoElement)

      // オプションが適切な構造を持つことを確認
      const playerOptions = { controls: true, fluid: true, ...options }
      if ('src' in playerOptions && !playerOptions.sources) {
        const src = playerOptions.src as string
        playerOptions.sources = [
          {
            src,
            type: src.includes('.m3u8') ? 'application/x-mpegURL' : 'video/mp4',
          },
        ]
        delete (playerOptions as Record<string, unknown>).src
      }

      const player = (playerRef.current = videojs(videoElement, playerOptions, () => {
        onReady?.(player)
      }))

      // prop変更時に既存のプレーヤーを更新
    } else if (playerRef.current) {
      const player = playerRef.current
      if (options.autoplay !== undefined) {
        player.autoplay(options.autoplay)
      }
      if (options.sources) {
        player.src(options.sources)
      }
    }
  }, [options, onReady])

  // 関数コンポーネントのアンマウント時にVideo.jsプレーヤーを破棄
  useEffect(() => {
    const player = playerRef.current
    return () => {
      if (player && !player.isDisposed()) {
        player.dispose()
        playerRef.current = null
      }
    }
  }, [])

  return (
    <div data-vjs-player>
      <div ref={videoRef} />
    </div>
  )
}
