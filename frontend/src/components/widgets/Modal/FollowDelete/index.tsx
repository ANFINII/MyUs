import { Channel } from 'types/internal/channle'
import AvatarLink from 'components/parts/Avatar/Link'
import Modal from 'components/parts/Modal'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'

export interface Props {
  open: boolean
  onClose: () => void
  onAction: () => void
  loading?: boolean
  channel: Channel
  followerCount: number
}

export default function FollowDeleteModal(props: Props): React.JSX.Element {
  const { open, onClose, onAction, loading, channel, followerCount } = props

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="フォロー解除"
      actions={[
        { name: '解除する', color: 'red', loading, onClick: onAction },
        { name: 'キャンセル', color: 'white', onClick: onClose },
      ]}
    >
      <div className="mb_8">こちらのユーザーのフォローを解除しますか？</div>
      <HStack gap="4">
        <AvatarLink src={channel.avatar} size="l" ulid={channel.ulid} nickname={channel.name} />
        <VStack gap="2">
          <p className="fs_14">{channel.name}</p>
          <p className="fs_14 text_sub">
            登録者数<span className="ml_8">{followerCount}</span>
          </p>
        </VStack>
      </HStack>
    </Modal>
  )
}
