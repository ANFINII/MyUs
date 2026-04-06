import { useRef, useState, useCallback, useEffect } from 'react'
import cx from 'utils/functions/cx'
import style from './AudioPlayer.module.scss'

const PLAY_EVENT = 'audioplayer:play'

const formatTime = (seconds: number): string => {
  if (!isFinite(seconds)) return '00:00'
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
}

interface Props {
  src: string
  playbackRate?: number
  className?: string
}

export default function AudioPlayer(props: Props): React.JSX.Element {
  const { src, playbackRate = 1, className } = props

  const audioRef = useRef<HTMLAudioElement>(null)
  const barRef = useRef<HTMLDivElement>(null)
  const volumeTrackRef = useRef<HTMLDivElement>(null)
  const isDraggingRef = useRef(false)
  const wasPlayingRef = useRef(false)
  const isVolumeDraggingRef = useRef(false)
  const [isPlaying, setIsPlaying] = useState(false)
  const [isMuted, setIsMuted] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [loaded, setLoaded] = useState(0)
  const [volume, setVolume] = useState(0.5)

  const seekToPosition = useCallback((clientX: number) => {
    const audio = audioRef.current
    const bar = barRef.current
    if (!audio || !bar || !isFinite(audio.duration)) return
    const rect = bar.getBoundingClientRect()
    const ratio = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width))
    audio.currentTime = ratio * audio.duration
  }, [])

  const setVolumeFromPosition = useCallback((clientY: number) => {
    const audio = audioRef.current
    const track = volumeTrackRef.current
    if (!audio || !track) return
    const rect = track.getBoundingClientRect()
    const newVolume = Math.max(0, Math.min(1, 1 - (clientY - rect.top) / rect.height))
    audio.volume = newVolume
    setVolume(newVolume)
    if (newVolume > 0 && audio.muted) {
      audio.muted = false
      setIsMuted(false)
    }
  }, [])

  const handlePlayPause = () => {
    const audio = audioRef.current
    if (!audio) return
    if (audio.paused) {
      audio.play()?.catch(() => {})
    } else {
      audio.pause()
    }
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
    setVolumeFromPosition(e.clientY)
  }

  const handleTimeUpdate = () => {
    if (audioRef.current) setCurrentTime(audioRef.current.currentTime)
  }

  const handleLoadedMetadata = () => {
    if (audioRef.current) setDuration(audioRef.current.duration)
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

  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return
    audio.playbackRate = playbackRate
    audio.volume = 0.5
  }, [playbackRate])

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (isDraggingRef.current) seekToPosition(e.clientX)
      if (isVolumeDraggingRef.current) setVolumeFromPosition(e.clientY)
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
    <div className={cx(style.player, isPlaying && style.playing, isMuted && style.muted, className)}>
      <div className={style.playpause} onClick={handlePlayPause}>
        <span className={style.icon} />
      </div>
      <div className={cx(style.time, style.timeCurrent)}>{formatTime(currentTime)}</div>
      <div className={style.bar} ref={barRef} onMouseDown={handleBarMouseDown}>
        <div className={style.barLoaded} style={{ width: `${loaded}%` }} />
        <div className={style.barPlayed} style={{ width: `${playedPercent}%` }} />
      </div>
      <div className={cx(style.time, style.timeDuration)}>{formatTime(duration)}</div>
      <div className={style.volume}>
        <div className={style.volumeButton} onClick={handleMuteToggle}>
          <span className={style.icon} />
        </div>
        <div className={style.volumeAdjust}>
          <div ref={volumeTrackRef} onMouseDown={handleVolumeMouseDown}>
            <div style={{ height: `${volume * 100}%` }} />
          </div>
        </div>
      </div>
      <audio
        ref={audioRef}
        src={src}
        preload="auto"
        onTimeUpdate={handleTimeUpdate}
        onLoadedMetadata={handleLoadedMetadata}
        onProgress={handleProgress}
        onPlay={handlePlay}
        onPause={handlePause}
        onEnded={handlePause}
      />
    </div>
  )
}
