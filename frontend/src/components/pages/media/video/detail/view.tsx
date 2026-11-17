import { lazy, Suspense } from 'react'
import { VideoDetailOut } from 'types/internal/media/output'
import { MediaPath } from 'utils/constants/enum'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import ExImage from 'components/parts/ExImage'
import MediaDetail from 'components/widgets/Media/Detail'
import MediaDetailCommon from 'components/widgets/Media/Detail/Common'

const VideoJS = lazy(() => import('components/widgets/Video/videojs'))

interface Props {
  data: VideoDetailOut
}

export default function VideoDetail(props: Props): React.JSX.Element {
  const { data } = props
  const { detail, list, series } = data
  const { image, video, publish, ...other } = detail

  const { toast, handleToast } = useToast()

  return (
    <Main metaTitle="Video" toast={toast}>
      <MediaDetail publish={publish}>
        <div className="media_detail_video">
          <div className="media_detail_contents">
            <Suspense fallback={<ExImage src={image} />}>
              <VideoJS
                options={{
                  src: video,
                  poster: image,
                  controls: true,
                  loop: false,
                  preload: 'auto',
                  controlBar: {
                    playToggle: true,
                    currentTimeDisplay: true,
                    timeDivider: true,
                    durationDisplay: true,
                    remainingTimeDisplay: false,
                    customControlSpacer: true,
                    chaptersButton: false,
                    descriptionsButton: false,
                    subsCapsButton: false,
                    audioTrackButton: false,
                    fullscreenToggle: true,
                  },
                  playbackRates: [0.5, 0.75, 1, 1.25, 1.5, 2],
                  loadingSpinner: true,
                  bigPlayButton: true,
                  errorDisplay: true,
                  userActions: { hotkeys: true },
                }}
              />
            </Suspense>
          </div>
        </div>
        <Divide />
        <MediaDetailCommon media={{ mediaPath: MediaPath.Video, ...other }} list={list} series={series} handleToast={handleToast} />
      </MediaDetail>
    </Main>
  )
}
