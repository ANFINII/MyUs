import { useContext } from 'react'
import { UserContext } from 'components/provider/UserProvider'

export function useUser() {
  const context = useContext(UserContext)
  if (!context) throw new Error()
  return context
}
