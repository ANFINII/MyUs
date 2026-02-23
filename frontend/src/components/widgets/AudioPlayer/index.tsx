import { useRef, useState, useCallback, useEffect } from 'react'
import clsx from 'clsx'
import style from './AudioPlayer.module.scss'

const formatTime = (seconds: number): string => {
  if (!isFinite(seconds)) return '00:00'
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
}

interface Props {
  src: string
  playbackRate?: number
}

export default function AudioPlayer(props: Props): React.JSX.Element {
  const { src, playbackRate = 1 } = props

  const audioRef = useRef<HTMLAudioElement>(null)
  const barRef = useRef<HTMLDivElement>(null)
  const volumeTrackRef = useRef<HTMLDivElement>(null)

  const [isPlaying, setIsPlaying] = useState(false)
  const [isMuted, setIsMuted] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [loaded, setLoaded] = useState(0)
  const [volume, setVolume] = useState(1)

  const handlePlayPause = useCallback(() => {
    const audio = audioRef.current
    if (!audio) return
    if (audio.paused) {
      audio.play()?.catch(() => {
        // 再生失敗を静かに処理
      })
    } else {
      audio.pause()
    }
  }, [])

  const handleBarClick = useCallback((e: React.MouseEvent<HTMLDivElement>) => {
    const audio = audioRef.current
    const bar = barRef.current
    if (!audio || !bar || !audio.duration) return
    const rect = bar.getBoundingClientRect()
    const ratio = (e.clientX - rect.left) / rect.width
    audio.currentTime = ratio * audio.duration
  }, [])

  const handleMuteToggle = useCallback(() => {
    const audio = audioRef.current
    if (!audio) return
    const newMuted = !audio.muted
    audio.muted = newMuted
    setIsMuted(newMuted)
  }, [])

  const handleVolumeClick = useCallback((e: React.MouseEvent<HTMLDivElement>) => {
    const audio = audioRef.current
    const track = volumeTrackRef.current
    if (!audio || !track) return
    const rect = track.getBoundingClientRect()
    const ratio = 1 - (e.clientY - rect.top) / rect.height
    const newVolume = Math.max(0, Math.min(1, ratio))
    audio.volume = newVolume
    setVolume(newVolume)
    if (newVolume > 0 && audio.muted) {
      audio.muted = false
      setIsMuted(false)
    }
  }, [])

  const handleTimeUpdate = useCallback(() => {
    const audio = audioRef.current
    if (audio) setCurrentTime(audio.currentTime)
  }, [])

  const handleLoadedMetadata = useCallback(() => {
    const audio = audioRef.current
    if (audio) setDuration(audio.duration)
  }, [])

  const handleProgress = useCallback(() => {
    const audio = audioRef.current
    if (!audio?.buffered.length || !audio.duration) return
    const buffered = audio.buffered.end(audio.buffered.length - 1)
    setLoaded((buffered / audio.duration) * 100)
  }, [])

  const handlePlay = useCallback(() => setIsPlaying(true), [])
  const handlePause = useCallback(() => setIsPlaying(false), [])

  useEffect(() => {
    const audio = audioRef.current
    if (audio) audio.playbackRate = playbackRate
  }, [playbackRate])

  const playedPercent = duration ? (currentTime / duration) * 100 : 0

  return (
    <div className={clsx(style.player, isPlaying && style.playing, isMuted && style.muted)}>
      <div className={style.playpause} onClick={handlePlayPause}>
        <span className={style.icon} />
      </div>
      <div className={clsx(style.time, style.timeCurrent)}>{formatTime(currentTime)}</div>
      <div className={style.bar} ref={barRef} onClick={handleBarClick}>
        <div className={style.barLoaded} style={{ width: `${loaded}%` }} />
        <div className={style.barPlayed} style={{ width: `${playedPercent}%` }} />
      </div>
      <div className={clsx(style.time, style.timeDuration)}>{formatTime(duration)}</div>
      <div className={style.volume}>
        <div className={style.volumeButton} onClick={handleMuteToggle}>
          <span className={style.icon} />
        </div>
        <div className={style.volumeAdjust}>
          <div ref={volumeTrackRef} onClick={handleVolumeClick}>
            <div style={{ height: `${volume * 100}%` }} />
          </div>
        </div>
      </div>
      <audio
        ref={audioRef}
        preload="metadata"
        onTimeUpdate={handleTimeUpdate}
        onLoadedMetadata={handleLoadedMetadata}
        onProgress={handleProgress}
        onPlay={handlePlay}
        onPause={handlePause}
        onEnded={handlePause}
      >
        <source src={src} />
      </audio>
    </div>
  )
}
