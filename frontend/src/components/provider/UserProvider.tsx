import { useState, createContext, useEffect, useCallback } from 'react'
import { UserMe } from 'types/internal/auth'
import { getUser } from 'api/internal/auth'

export interface UserContextType {
  user: UserMe
  updateUser: () => Promise<void>
  resetUser: () => Promise<void>
}

export const UserContext = createContext<UserContextType | undefined>(undefined)

const initUser = { avatar: '', ulid: '', email: '', nickname: '', isActive: false, isStaff: false }

interface Props {
  children: React.ReactNode
}

export function UserProvider(props: Props): React.JSX.Element {
  const { children } = props

  const [user, setUser] = useState<UserMe>(initUser)

  const resetUser = async () => setUser(initUser)

  const updateUser = useCallback(async () => {
    const ret = await getUser()
    if (ret.isErr()) return resetUser()
    setUser(ret.value)
  }, [])

  useEffect(() => {
    const fetchUser = async () => updateUser()
    fetchUser()
  }, [updateUser])

  const value = { user, updateUser, resetUser }
  return <UserContext.Provider value={value}>{children}</UserContext.Provider>
}
