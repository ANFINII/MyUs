import { useRef, useState, useCallback, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { RepeatMode } from 'types/internal/other'
import cx from 'utils/functions/cx'
import { formatTime } from 'utils/functions/datetime'
import { gainVolume, getVolume, saveVolume } from 'utils/functions/volume'
import IconRepeat from 'components/parts/Icon/Repeat'
import IconSkip from 'components/parts/Icon/Skip'
import style from './AudioPlayer.module.scss'

const PLAY_EVENT = 'audioplayer:play'
const SKIP_SECONDS = 10

interface Props {
  src: string
  gain?: number
  playbackRate?: number
  autoPlay?: boolean
  isVolumeInline?: boolean
  repeat?: RepeatMode
  audioRef?: React.RefObject<HTMLAudioElement | null>
  className?: string
  onEnded?: () => void
  onRepeat?: () => void
  onTimeUpdate?: (time: number) => void
}

export default function AudioPlayer(props: Props): React.JSX.Element {
  const { src, gain = 0, playbackRate = 1, autoPlay = false, isVolumeInline = false, repeat = 'off', audioRef: sharedAudioRef, className, onEnded, onRepeat, onTimeUpdate } = props

  const { t } = useTranslation()
  const audioRef = useRef<HTMLAudioElement>(null)
  const barRef = useRef<HTMLDivElement>(null)
  const volumeTrackRef = useRef<HTMLDivElement>(null)
  const isDraggingRef = useRef(false)
  const wasPlayingRef = useRef(false)
  const isVolumeDraggingRef = useRef(false)
  const [isPlaying, setIsPlaying] = useState<boolean>(false)
  const [isMuted, setIsMuted] = useState<boolean>(false)
  const [currentTime, setCurrentTime] = useState<number>(0)
  const [duration, setDuration] = useState<number>(0)
  const [loaded, setLoaded] = useState<number>(0)
  const [volume, setVolume] = useState<number>(getVolume())

  const seekToPosition = useCallback((clientX: number) => {
    const audio = audioRef.current
    const bar = barRef.current
    if (!audio || !bar || !isFinite(audio.duration)) return
    const rect = bar.getBoundingClientRect()
    const ratio = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width))
    audio.currentTime = ratio * audio.duration
  }, [])

  const setVolumeFromPosition = useCallback(
    (clientX: number, clientY: number) => {
      const audio = audioRef.current
      const track = volumeTrackRef.current
      if (!audio || !track) return
      const rect = track.getBoundingClientRect()
      const ratio = isVolumeInline ? (clientX - rect.left) / rect.width : 1 - (clientY - rect.top) / rect.height
      const newVolume = Math.max(0, Math.min(1, ratio))
      audio.volume = gainVolume(newVolume, gain)
      setVolume(newVolume)
      saveVolume(newVolume)
      if (newVolume > 0 && audio.muted) {
        audio.muted = false
        setIsMuted(false)
      }
    },
    [isVolumeInline, gain],
  )

  const handlePlayPause = () => {
    const audio = audioRef.current
    if (!audio) return
    if (audio.paused) {
      audio.play()?.catch(() => {})
    } else {
      audio.pause()
    }
  }

  const handleSkip = (seconds: number) => () => {
    const audio = audioRef.current
    if (!audio || !isFinite(audio.duration)) return
    audio.currentTime = Math.max(0, Math.min(audio.duration, audio.currentTime + seconds))
  }

  const handleBarMouseDown = (e: React.MouseEvent<HTMLDivElement>) => {
    const audio = audioRef.current
    isDraggingRef.current = true
    wasPlayingRef.current = !!audio && !audio.paused
    audio?.pause()
    seekToPosition(e.clientX)
  }

  const handleMuteToggle = () => {
    const audio = audioRef.current
    if (!audio) return
    audio.muted = !audio.muted
    setIsMuted(audio.muted)
  }

  const handleVolumeMouseDown = (e: React.MouseEvent<HTMLDivElement>) => {
    isVolumeDraggingRef.current = true
    setVolumeFromPosition(e.clientX, e.clientY)
  }

  const handleTimeUpdate = () => {
    const audio = audioRef.current
    if (!audio) return
    setCurrentTime(audio.currentTime)
    onTimeUpdate?.(audio.currentTime)
  }

  const handleLoadedMetadata = () => {
    const audio = audioRef.current
    if (!audio) return
    audio.volume = gainVolume(volume, gain)
    setDuration(audio.duration)
  }

  const handleProgress = () => {
    const audio = audioRef.current
    if (!audio?.buffered.length || !audio.duration) return
    setLoaded((audio.buffered.end(audio.buffered.length - 1) / audio.duration) * 100)
  }

  const handlePlay = () => {
    setIsPlaying(true)
    window.dispatchEvent(new CustomEvent(PLAY_EVENT, { detail: audioRef.current }))
  }

  const handlePause = () => setIsPlaying(false)

  const handleAudioRef = (audio: HTMLAudioElement | null) => {
    audioRef.current = audio
    if (sharedAudioRef) sharedAudioRef.current = audio
  }

  const handleEnded = () => {
    setIsPlaying(false)
    onEnded?.()
  }

  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return
    audio.playbackRate = playbackRate
  }, [playbackRate])

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (isDraggingRef.current) seekToPosition(e.clientX)
      if (isVolumeDraggingRef.current) setVolumeFromPosition(e.clientX, e.clientY)
    }
    const handleMouseUp = () => {
      if (isDraggingRef.current && wasPlayingRef.current) {
        audioRef.current?.play()?.catch(() => {})
      }
      isDraggingRef.current = false
      isVolumeDraggingRef.current = false
    }
    window.addEventListener('mousemove', handleMouseMove)
    window.addEventListener('mouseup', handleMouseUp)
    return () => {
      window.removeEventListener('mousemove', handleMouseMove)
      window.removeEventListener('mouseup', handleMouseUp)
    }
  }, [seekToPosition, setVolumeFromPosition])

  useEffect(() => {
    const handleGlobalPlay = (e: Event) => {
      const audio = audioRef.current
      if (audio && (e as CustomEvent).detail !== audio) audio.pause()
    }
    window.addEventListener(PLAY_EVENT, handleGlobalPlay)
    return () => window.removeEventListener(PLAY_EVENT, handleGlobalPlay)
  }, [])

  const playedPercent = duration ? (currentTime / duration) * 100 : 0

  return (
    <div className={cx(style.player, isPlaying && style.playing, isMuted && style.muted, isVolumeInline && style.volume_inline, onRepeat && style.repeatable, className)}>
      <div className={style.playpause} onClick={handlePlayPause}>
        <span className={style.icon} />
      </div>
      <div className={style.bar} ref={barRef} onMouseDown={handleBarMouseDown}>
        <div className={style.bar_loaded} style={{ width: `${loaded}%` }} />
        <div className={style.bar_played} style={{ width: `${playedPercent}%` }} />
        <span className={style.bar_time}>
          <span>{formatTime(currentTime)}</span>
          <span>{formatTime(duration)}</span>
        </span>
      </div>
      <div className={cx(style.skip, style.skip_back)} onClick={handleSkip(-SKIP_SECONDS)}>
        <IconSkip size="1.2em" type="back" />
      </div>
      <div className={cx(style.skip, style.skip_forward)} onClick={handleSkip(SKIP_SECONDS)}>
        <IconSkip size="1.2em" type="forward" />
      </div>
      {onRepeat && (
        <div title={t(`player.repeat.${repeat}`)} className={cx(style.skip, style.repeat, repeat !== 'off' && style.active)} onClick={onRepeat}>
          <IconRepeat size="1.2em" type={repeat === 'one' ? 'one' : 'all'} />
        </div>
      )}
      <div className={style.volume}>
        <div className={style.volume_button} onClick={handleMuteToggle}>
          <span className={style.icon} />
        </div>
        <div className={style.volume_adjust}>
          <div ref={volumeTrackRef} onMouseDown={handleVolumeMouseDown}>
            <div style={isVolumeInline ? { width: `${volume * 100}%` } : { height: `${volume * 100}%` }} />
          </div>
        </div>
      </div>
      <audio
        ref={handleAudioRef}
        src={src}
        preload="auto"
        autoPlay={autoPlay}
        loop={repeat === 'one'}
        onTimeUpdate={handleTimeUpdate}
        onLoadedMetadata={handleLoadedMetadata}
        onProgress={handleProgress}
        onPlay={handlePlay}
        onPause={handlePause}
        onEnded={handleEnded}
      />
    </div>
  )
}
