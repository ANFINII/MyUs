import { useState, createContext, useEffect } from 'react'
import { getUser } from 'api/auth'
import { UserMe } from 'types/internal/auth'

export interface UserContextType {
  user: UserMe
  updateUser: () => Promise<void>
  resetUser: () => void
}

export const UserContext = createContext<UserContextType | undefined>(undefined)

const initUser = { avatar: '', email: '', nickname: '', isActive: false, isStaff: false }

interface Props {
  children: React.ReactNode
}

export function UserProvider(props: Props) {
  const { children } = props

  const [user, setUser] = useState<UserMe>(initUser)

  const resetUser = () => setUser(initUser)
  const updateUser = async () => setUser(await getUser())

  useEffect(() => {
    const fetchUser = async () => {
      try {
        await updateUser()
      } catch (e) {
        setUser(initUser)
      }
    }
    fetchUser()
  }, [])

  const value = { user, updateUser, resetUser }
  return <UserContext.Provider value={value}>{children}</UserContext.Provider>
}
