import { useTranslation } from 'react-i18next'
import { Channel } from 'types/internal/channel'
import AvatarLink from 'components/parts/Avatar/Link'
import Modal from 'components/parts/Modal'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'

interface Props {
  open: boolean
  onClose: () => void
  onAction: () => void
  loading?: boolean
  channel: Channel
  followerCount: number
}

export default function SubscribeDeleteModal(props: Props): React.JSX.Element {
  const { open, onClose, onAction, loading, channel, followerCount } = props

  const { t } = useTranslation()

  return (
    <Modal
      open={open}
      onClose={onClose}
      title={t('modal.subscribeDelete.title')}
      actions={[
        { name: t('modal.subscribeDelete.action'), color: 'red', loading, onClick: onAction },
        { name: t('action.cancel'), color: 'white', onClick: onClose },
      ]}
    >
      <div className="mb_8">{t('modal.subscribeDelete.confirm')}</div>
      <HStack gap="4">
        <AvatarLink size="l" src={channel.avatar} ulid={channel.ownerUlid} title={channel.name} />
        <VStack gap="2">
          <p className="fs_14">{channel.name}</p>
          <p className="fs_14 text_sub">
            {t('count.subscribers')}
            <span className="ml_8">{followerCount}</span>
          </p>
        </VStack>
      </HStack>
    </Modal>
  )
}
