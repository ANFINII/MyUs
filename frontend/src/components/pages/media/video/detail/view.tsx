import { lazy, Suspense, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { globalAdvertisesQuery } from 'lib/query/options'
import { Advertise } from 'types/internal/advertise'
import { VideoDetailOut } from 'types/internal/media/output'
import { MediaPath } from 'utils/constants/enum'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import ExImage from 'components/parts/ExImage'
import AdvertiseVideo from 'components/widgets/AdvertiseVideo'
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
  const globalAdvertises = useQuery(globalAdvertisesQuery())
  const [advertise, setAdvertise] = useState<Advertise | null>(globalAdvertises.data?.items.find((item) => item.video !== '') ?? null)
  const [isAutoplay, setIsAutoplay] = useState<boolean>(false)

  const handleAdvertiseEnd = () => {
    setAdvertise(null)
    setIsAutoplay(true)
  }

  return (
    <Main metaTitle="Video" toast={toast}>
      <MediaDetail publish={publish}>
        <div className="media_detail_video">
          <div className="media_detail_contents">
            {advertise !== null ? (
              <AdvertiseVideo item={advertise} onEnd={handleAdvertiseEnd} />
            ) : (
              <Suspense fallback={<ExImage src={image} />}>
                <VideoJS
                  options={{
                    src: video,
                    poster: image,
                    autoplay: isAutoplay,
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
            )}
          </div>
        </div>
        <Divide />
        <MediaDetailCommon media={{ mediaPath: MediaPath.Video, ...other }} list={list} series={series} handleToast={handleToast} />
      </MediaDetail>
    </Main>
  )
}
