import { useContext } from 'react'
import { UserContext, UserContextType } from 'components/provider/UserProvider'

export function useUser(): UserContextType {
  const context = useContext(UserContext)
  if (!context) throw new Error()
  return context
}
