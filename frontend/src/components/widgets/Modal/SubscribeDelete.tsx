import { useTranslation } from 'react-i18next'
import { Channel } from 'types/internal/channel'
import Modal from 'components/parts/Modal'
import ProfileInfo from 'components/widgets/ProfileInfo'

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
      <ProfileInfo avatar={channel.avatar} ulid={channel.ownerUlid} name={channel.name} countLabel={t('count.subscribers')} count={followerCount} />
    </Modal>
  )
}
