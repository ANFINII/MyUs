import { useRef, useEffect } from 'react'
import videojs from 'video.js'
import 'videojs-contrib-quality-levels'
import 'videojs-hls-quality-selector'

type Player = ReturnType<typeof videojs>
type PlayerOptions = Parameters<typeof videojs>[1]

interface QualityLevel {
  enabled: boolean
  height: number
  width: number
  bitrate: number
}

interface QualityLevels {
  length: number
  selectedIndex: number
  [index: number]: QualityLevel
  on(event: string, callback: () => void): void
}

interface ExtendedPlayer extends Player {
  qualityLevels(): QualityLevels
  hlsQualitySelector(options?: { displayCurrentQuality?: boolean; sort?: 'high-to-low' | 'low-to-high' }): void
}

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
        const extendedPlayer = player as ExtendedPlayer
        extendedPlayer.hlsQualitySelector({ displayCurrentQuality: true })
        setTimeout(() => {
          const reorderQualityMenu = () => {
            const qualityButton = player.el().querySelector('.vjs-quality-selector')
            if (qualityButton) {
              const menu = qualityButton.querySelector('.vjs-menu')
              const menuContent = menu?.querySelector('.vjs-menu-content')
              if (menuContent) {
                const menuItems = Array.from(menuContent.querySelectorAll('.vjs-menu-item'))
                if (menuItems.length > 1) {
                  const sortedItems = [...menuItems].sort((a, b) => {
                    const aText = (a.textContent || '').trim()
                    const bText = (b.textContent || '').trim()
                    if (aText.includes('Auto')) return 1
                    if (bText.includes('Auto')) return -1
                    const aMatch = aText.match(/(\d+)p/)
                    const bMatch = bText.match(/(\d+)p/)
                    if (aMatch && bMatch && aMatch[1] && bMatch[1]) {
                      return parseInt(bMatch[1]) - parseInt(aMatch[1])
                    }
                    return 0
                  })
                  sortedItems.forEach((item) => menuContent.appendChild(item))
                }
              }
            }
          }
          reorderQualityMenu()
          setTimeout(reorderQualityMenu, 500)
          setTimeout(reorderQualityMenu, 1000)
          setTimeout(reorderQualityMenu, 2000)
        }, 100)
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
