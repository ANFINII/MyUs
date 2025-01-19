import { useState, createContext, useEffect } from 'react'
import { UserMe } from 'types/internal/auth'
import { getUser } from 'api/internal/auth'

export interface UserContextType {
  user: UserMe
  updateUser: () => Promise<void>
  resetUser: () => Promise<void>
}

export const UserContext = createContext<UserContextType | undefined>(undefined)

const initUser = { avatar: '', email: '', nickname: '', isActive: false, isStaff: false }

interface Props {
  children: React.ReactNode
}

export function UserProvider(props: Props): JSX.Element {
  const { children } = props

  const [user, setUser] = useState<UserMe>(initUser)

  const updateUser = async () => setUser(await getUser())
  const resetUser = async () => setUser(initUser)

  useEffect(() => {
    const fetchUser = async () => {
      try {
        await updateUser()
      } catch {
        await resetUser()
      }
    }
    fetchUser()
  }, [])

  const value = { user, updateUser, resetUser }
  return <UserContext.Provider value={value}>{children}</UserContext.Provider>
}
