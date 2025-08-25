import { useRef } from 'react'
import Player from 'video.js/dist/types/player'
import { VideoDetailOut } from 'types/internal/media/detail'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import VStack from 'components/parts/Stack/Vertical'
import MediaDetail from 'components/widgets/Media/Detail'
import MediaDetailCommon from 'components/widgets/Media/Detail/Common'
import MediaSideImage from 'components/widgets/Media/Side/Image'
import VideoJS from 'components/widgets/Video/videojs'

interface QualityLevels {
  length: number
  on: (event: string, callback: () => void) => void
}

type PlayerWithQuality = Player & {
  qualityLevels?: () => QualityLevels
}

interface Props {
  status: number
  data: VideoDetailOut
}

export default function VideoDetail(props: Props): JSX.Element {
  const { data } = props
  const { detail, list } = data
  const { image, convert, publish, ...other } = detail

  const { toast, handleToast } = useToast()

  const playerRef = useRef<Player | null>(null)

  const handlePlayerReady = (player: Player) => {
    playerRef.current = player

    // 解像度選択メニューを追加（複数の解像度がある場合）
    const playerWithQuality = player as PlayerWithQuality
    if (playerWithQuality.qualityLevels && typeof playerWithQuality.qualityLevels === 'function') {
      const qualityLevels = playerWithQuality.qualityLevels()

      // 解像度が複数ある場合のみメニューを表示
      if (qualityLevels && qualityLevels.length > 1) {
        // qualityLevelsプラグインが利用可能な場合の処理
        qualityLevels.on('addqualitylevel', () => {
          // 解像度が追加された時の処理
        })
      }
    }
  }

  return (
    <Main metaTitle="Video" toast={toast}>
      <MediaDetail publish={publish}>
        <div className="media_detail_video">
          <div className="media_detail_contents">
            <VideoJS
              onReady={handlePlayerReady}
              options={{
                src: convert,
                poster: image,
                width: 544,
                height: 306,
                muted: false,
                controls: true,
                autoplay: false,
                loop: false,
                preload: 'auto',
                controlBar: {
                  playToggle: true,
                  volumePanel: {
                    inline: false,
                    vertical: true,
                  },
                  currentTimeDisplay: true,
                  timeDivider: true,
                  durationDisplay: true,
                  progressControl: {
                    seekBar: {
                      loadProgressBar: true,
                      mouseTimeDisplay: true,
                      playProgressBar: true,
                    },
                  },
                  remainingTimeDisplay: false,
                  customControlSpacer: true,
                  playbackRateMenuButton: {
                    playbackRates: [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2],
                  },
                  chaptersButton: false,
                  descriptionsButton: false,
                  subsCapsButton: false,
                  audioTrackButton: false,
                  fullscreenToggle: true,
                },
                playbackRates: [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2],
                loadingSpinner: true,
                bigPlayButton: true,
                errorDisplay: true,
                userActions: {
                  hotkeys: true,
                },
              }}
            />
          </div>
        </div>
        <Divide />
        <div className="media_detail_grid">
          <MediaDetailCommon media={{ type: 'video', ...other }} handleToast={handleToast} />
          <VStack gap="4" className="ml_20">
            {list.map((media) => (
              <MediaSideImage key={media.id} href={`/media/video/${media.id}`} src={media.image} media={media} />
            ))}
          </VStack>
        </div>
      </MediaDetail>
    </Main>
  )
}
