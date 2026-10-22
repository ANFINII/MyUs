import { useContext } from 'react'
import { ToastContext, ToastContextType } from 'components/provider/ToastProvider'

export function useToast(): ToastContextType {
  const context = useContext(ToastContext)
  if (!context) throw new Error('useToast は ToastProvider の中で使う')
  return context
}
