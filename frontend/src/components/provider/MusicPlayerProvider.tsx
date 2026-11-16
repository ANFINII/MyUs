import { useState, createContext } from 'react'
import { Music } from 'types/internal/media/output'

export interface MusicPlayerContextType {
  current: Music | undefined
  play: (queue: Music[], index: number) => void
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

  const [queue, setQueue] = useState<Music[]>([])
  const [index, setIndex] = useState<number>(0)

  const current = queue[index]

  const play = (items: Music[], i: number) => {
    setQueue(items)
    setIndex(i)
  }

  const next = () => setIndex((i) => (i + 1 < queue.length ? i + 1 : i))
  const prev = () => setIndex((i) => (i > 0 ? i - 1 : i))
  const close = () => setQueue([])

  const value = { current, play, next, prev, close }
  return <MusicPlayerContext.Provider value={value}>{children}</MusicPlayerContext.Provider>
}
