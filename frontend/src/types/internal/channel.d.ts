export interface Channel {
  ulid: string
  ownerUlid: string
  avatar: string
  name: string
  isDefault: boolean
  description: string
}

export interface ChannelIn {
  name: string
  avatarFile?: File
  description: string
}
