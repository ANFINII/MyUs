import { Channel } from 'types/internal/channel'

export const selectChannelUlid = (channels: Channel[], ulid?: string): string => {
  return (channels.find((c) => c.ulid === ulid) ?? channels.find((c) => c.isDefault))?.ulid ?? ''
}
