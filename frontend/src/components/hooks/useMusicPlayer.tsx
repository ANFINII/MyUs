import { useContext } from 'react'
import { MusicPlayerContext, MusicPlayerContextType } from 'components/provider/MusicPlayerProvider'

export function useMusicPlayer(): MusicPlayerContextType {
  const context = useContext(MusicPlayerContext)
  if (!context) throw new Error('useMusicPlayer は MusicPlayerProvider の中で使う')
  return context
}
