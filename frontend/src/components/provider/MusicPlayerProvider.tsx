import { useRef, useState, createContext } from 'react'
import { Music } from 'types/internal/media/output'

export interface MusicPlayerContextType {
  current: Music | undefined
  audioRef: React.RefObject<HTMLAudioElement | null>
  play: (queue: Music[], index: number) => void
  toggle: () => void
  next: () => void
  prev: () => void
  close: () => void
}

export const MusicPlayerContext = createContext<MusicPlayerContextType | undefined>(undefined)

interface Props {
  children: React.ReactNode
}

export function MusicPlayerProvider(props: Props): React.JSX.Element {
  const { children } = props

  const audioRef = useRef<HTMLAudioElement>(null)
  const [queue, setQueue] = useState<Music[]>([])
  const [index, setIndex] = useState<number>(0)

  const current = queue[index]

  const play = (items: Music[], i: number) => {
    setQueue(items)
    setIndex(i)
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

  const next = () => setIndex((i) => (i + 1 < queue.length ? i + 1 : i))
  const prev = () => setIndex((i) => (i > 0 ? i - 1 : i))
  const close = () => setQueue([])

  const value = { current, audioRef, play, toggle, next, prev, close }
  return <MusicPlayerContext.Provider value={value}>{children}</MusicPlayerContext.Provider>
}
