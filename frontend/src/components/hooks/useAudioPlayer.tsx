import { useContext } from 'react'
import { AudioPlayerContext, AudioPlayerContextType } from 'components/provider/AudioPlayerProvider'

export function useAudioPlayer(): AudioPlayerContextType {
  const context = useContext(AudioPlayerContext)
  if (!context) throw new Error('useAudioPlayer は AudioPlayerProvider の中で使う')
  return context
}
