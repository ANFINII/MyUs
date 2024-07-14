import { useState, createContext } from 'react'
import { UserInfo } from 'types/internal/auth'

export interface UserContextType {
  user: UserInfo
  setUser: React.Dispatch<React.SetStateAction<UserInfo>>
}

export const UserContext = createContext<UserContextType | undefined>(undefined)

interface Props {
  children: React.ReactNode
}

export function UserProvider(props: Props) {
  const { children } = props
  const [user, setUser] = useState<UserInfo>({ avatar: '', email: '', nickname: '', isActive: false, isStaff: false })
  const value = { user, setUser }
  return <UserContext.Provider value={value}>{children}</UserContext.Provider>
}
