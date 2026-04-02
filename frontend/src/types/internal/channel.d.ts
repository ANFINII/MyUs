export interface Channel {
  ulid: string
  ownerUlid: string
  avatar: string
  name: string
  isDefault: boolean
  description: string
  count: number
}

export interface ChannelIn {
  name: string
  avatarFile?: File
  description: string
}

export interface SubscribeIn {
  channelUlid: string
  isSubscribe: boolean
}

export interface SubscribeOut {
  isSubscribe: boolean
  count: number
}
