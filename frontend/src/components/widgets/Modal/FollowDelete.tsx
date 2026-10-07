import { useTranslation } from 'react-i18next'
import AvatarLink from 'components/parts/Avatar/Link'
import Modal from 'components/parts/Modal'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'

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
      <HStack gap="4">
        <AvatarLink size="l" src={avatar} ulid={ulid} title={nickname} />
        <VStack gap="2">
          <p className="fs_14">{nickname}</p>
          <p className="fs_14 text_sub">
            {t('modal.followDelete.followers')}
            <span className="ml_8">{followerCount}</span>
          </p>
        </VStack>
      </HStack>
    </Modal>
  )
}
