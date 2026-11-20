import { useRef, useState, createContext, useCallback } from 'react'
import { Audio } from 'types/internal/media/output'
import { RepeatMode } from 'types/internal/other'
import { shuffleItems } from 'utils/functions/common'

export interface AudioPlayerContextType {
  current: Audio | undefined
  audioRef: React.RefObject<HTMLAudioElement | null>
  isShuffle: boolean
  repeat: RepeatMode
  play: (queue: Audio[], index: number) => void
  playShuffle: (queue: Audio[]) => void
  toggle: () => void
  next: () => void
  prev: () => void
  toggleShuffle: () => void
  toggleRepeat: () => void
  close: () => void
}

export const AudioPlayerContext = createContext<AudioPlayerContextType | undefined>(undefined)

const NEXT_REPEAT: Record<RepeatMode, RepeatMode> = { off: 'all', all: 'one', one: 'off' }

const shuffleFrom = (items: Audio[], first: Audio): Audio[] => [first, ...shuffleItems(items.filter((m) => m.ulid !== first.ulid))]

interface Props {
  children: React.ReactNode
}

export function AudioPlayerProvider(props: Props): React.JSX.Element {
  const { children } = props

  const audioRef = useRef<HTMLAudioElement>(null)
  const [original, setOriginal] = useState<Audio[]>([])
  const [queue, setQueue] = useState<Audio[]>([])
  const [index, setIndex] = useState<number>(0)
  const [isShuffle, setIsShuffle] = useState<boolean>(false)
  const [repeat, setRepeat] = useState<RepeatMode>('off')

  const current = queue[index]

  const play = (items: Audio[], i: number) => {
    const first = items[i]
    setOriginal(items)
    if (isShuffle && first) {
      setQueue(shuffleFrom(items, first))
      setIndex(0)
      return
    }
    setQueue(items)
    setIndex(i)
  }

  const playShuffle = (items: Audio[]) => {
    setIsShuffle(true)
    setOriginal(items)
    setQueue(shuffleItems(items))
    setIndex(0)
  }

  const toggle = () => {
    const audio = audioRef.current
    if (!audio) return
    if (audio.paused) {
      audio.play()?.catch(() => {})
    } else {
      audio.pause()
    }
  }

  const replay = () => {
    const audio = audioRef.current
    if (!audio) return
    audio.currentTime = 0
    audio.play()?.catch(() => {})
  }

  const next = () => {
    if (index + 1 < queue.length) return setIndex(index + 1)
    if (repeat === 'off') return
    if (queue.length === 1) return replay()
    setIndex(0)
  }

  const prev = () => setIndex((i) => (i > 0 ? i - 1 : i))

  const toggleShuffle = () => {
    setIsShuffle(!isShuffle)
    if (!current) return
    if (isShuffle) {
      setQueue(original)
      setIndex(Math.max(original.findIndex((m) => m.ulid === current.ulid), 0))
      return
    }
    setQueue(shuffleFrom(queue, current))
    setIndex(0)
  }

  const toggleRepeat = () => setRepeat(NEXT_REPEAT[repeat])

  const close = useCallback(() => setQueue([]), [])

  const value = { current, audioRef, isShuffle, repeat, play, playShuffle, toggle, next, prev, toggleShuffle, toggleRepeat, close }
  return <AudioPlayerContext.Provider value={value}>{children}</AudioPlayerContext.Provider>
}
