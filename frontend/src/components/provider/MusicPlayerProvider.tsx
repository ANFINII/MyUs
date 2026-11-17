import { useRef, useState, createContext, useCallback } from 'react'
import { Music } from 'types/internal/media/output'
import { shuffleItems } from 'utils/functions/common'

export type RepeatMode = 'off' | 'all' | 'one'

export interface MusicPlayerContextType {
  current: Music | undefined
  audioRef: React.RefObject<HTMLAudioElement | null>
  isShuffle: boolean
  repeat: RepeatMode
  play: (queue: Music[], index: number) => void
  playShuffle: (queue: Music[]) => void
  toggle: () => void
  next: () => void
  prev: () => void
  ended: () => void
  toggleShuffle: () => void
  toggleRepeat: () => void
  close: () => void
}

export const MusicPlayerContext = createContext<MusicPlayerContextType | undefined>(undefined)

const NEXT_REPEAT: Record<RepeatMode, RepeatMode> = { off: 'all', all: 'one', one: 'off' }

const shuffleFrom = (items: Music[], first: Music): Music[] => [first, ...shuffleItems(items.filter((m) => m.ulid !== first.ulid))]

interface Props {
  children: React.ReactNode
}

export function MusicPlayerProvider(props: Props): React.JSX.Element {
  const { children } = props

  const audioRef = useRef<HTMLAudioElement>(null)
  const [original, setOriginal] = useState<Music[]>([])
  const [queue, setQueue] = useState<Music[]>([])
  const [index, setIndex] = useState<number>(0)
  const [isShuffle, setIsShuffle] = useState<boolean>(false)
  const [repeat, setRepeat] = useState<RepeatMode>('off')

  const current = queue[index]

  const play = (items: Music[], i: number) => {
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

  const playShuffle = (items: Music[]) => {
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

  const ended = () => {
    if (repeat === 'one') return replay()
    next()
  }

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

  const value = { current, audioRef, isShuffle, repeat, play, playShuffle, toggle, next, prev, ended, toggleShuffle, toggleRepeat, close }
  return <MusicPlayerContext.Provider value={value}>{children}</MusicPlayerContext.Provider>
}
