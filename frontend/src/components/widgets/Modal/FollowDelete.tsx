import { useTranslation } from 'react-i18next'
import Modal from 'components/parts/Modal'
import ProfileInfo from 'components/widgets/ProfileInfo'

export interface Props {
  open: boolean
  onClose: () => void
  onAction: () => void
  loading?: boolean
  avatar: string
  ulid: string
  nickname: string
  followerCount: number
}

export default function FollowDeleteModal(props: Props): React.JSX.Element {
  const { open, onClose, onAction, loading, avatar, ulid, nickname, followerCount } = props

  const { t } = useTranslation()

  return (
    <Modal
      open={open}
      onClose={onClose}
      title={t('modal.followDelete.title')}
      actions={[
        { name: t('modal.followDelete.action'), color: 'red', loading, onClick: onAction },
        { name: t('action.cancel'), color: 'white', onClick: onClose },
      ]}
    >
      <div className="mb_8">{t('modal.followDelete.confirm')}</div>
      <ProfileInfo avatar={avatar} ulid={ulid} name={nickname} countLabel={t('modal.followDelete.followers')} count={followerCount} />
    </Modal>
  )
}
