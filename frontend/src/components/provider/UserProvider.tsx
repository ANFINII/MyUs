import { useState, createContext, useEffect, useCallback } from 'react'
import { UserMe } from 'types/internal/user'
import { getUser } from 'api/internal/user'

export interface UserContextType {
  user: UserMe
  resetUser: () => void
  updateUser: () => Promise<void>
}

export const UserContext = createContext<UserContextType | undefined>(undefined)

const initUser = { avatar: '', ulid: '', nickname: '', isActive: false, isStaff: false }

interface Props {
  children: React.ReactNode
}

export function UserProvider(props: Props): React.JSX.Element {
  const { children } = props

  const [user, setUser] = useState<UserMe>(initUser)

  const resetUser = useCallback(() => setUser(initUser), [])

  const updateUser = useCallback(async () => {
    const ret = await getUser()
    if (ret.isErr()) return resetUser()
    setUser(ret.value)
  }, [resetUser])

  useEffect(() => {
    updateUser()
  }, [updateUser])

  const value = { user, resetUser, updateUser }
  return <UserContext.Provider value={value}>{children}</UserContext.Provider>
}
