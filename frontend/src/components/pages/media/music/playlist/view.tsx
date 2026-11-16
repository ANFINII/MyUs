import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { errorMessage } from 'lib/error'
import { PlaylistList } from 'types/internal/playlist'
import { postPlaylist } from 'api/internal/playlist'
import { FetchError } from 'utils/constants/enum'
import { useLoading } from 'components/hooks/useLoading'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import { useUser } from 'components/hooks/useUser'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import CheckBox from 'components/parts/Input/CheckBox'
import Link from 'components/parts/Link'
import Modal from 'components/parts/Modal'
import CardList from 'components/widgets/Card/List'
import PlaylistCard from 'components/widgets/Card/Playlist'
import style from './Playlist.module.scss'
import MusicTabs from '../MusicTabs'

interface Props {
  data: PlaylistList
}

export default function Playlists(props: Props): React.JSX.Element {
  const { data } = props
  const { items } = data

  const router = useRouter()
  const { t } = useTranslation()
  const { user } = useUser()
  const { loading, handleLoading } = useLoading()
  const { toast, handleToast } = useToast()
  const [isModal, setIsModal] = useState<boolean>(false)
  const [title, setTitle] = useState<string>('')
  const [isPublish, setIsPublish] = useState<boolean>(false)

  const handleModal = () => setIsModal(!isModal)
  const handleTitle = (e: ChangeEvent<HTMLInputElement>) => setTitle(e.target.value)
  const handlePublish = (e: ChangeEvent<HTMLInputElement>) => setIsPublish(e.target.checked)

  const handleCreate = async () => {
    handleLoading(true)
    const ret = await postPlaylist({ title, publish: isPublish, musicUlid: '' })
    handleLoading(false)
    if (ret.isErr()) return handleToast(errorMessage(ret.error, FetchError.Post), true)
    router.push(`/media/music/playlist/${ret.value.ulid}`)
  }

  return (
    <Main title="Music" toast={toast}>
      <MusicTabs selected="playlist" />
      {user.isActive ? (
        <>
          <div className={style.toolbar}>
            <Button name={t('playlist.new')} color="green" size="s" onClick={handleModal} />
          </div>
          {items.length > 0 ? <CardList items={items} Content={PlaylistCard} /> : <p className={style.empty}>{t('playlist.empty')}</p>}
        </>
      ) : (
        <div className={style.login}>
          <p>{t('playlist.loginRequired')}</p>
          <Link href="/account/login" className={style.login_link}>
            {t('playlist.login')}
          </Link>
        </div>
      )}

      <Modal
        open={isModal}
        onClose={handleModal}
        title={t('playlist.new')}
        size="s"
        actions={[
          { name: t('action.cancel'), color: 'white', disabled: loading, onClick: handleModal },
          { name: t('playlist.createOnly'), color: 'blue', loading, disabled: title.trim() === '', onClick: handleCreate },
        ]}
      >
        <div className={style.form}>
          <Input label={t('playlist.newTitle')} value={title} maxLength={100} onChange={handleTitle} />
          <CheckBox label={t('playlist.publish')} id="playlist_publish_new" checked={isPublish} onChange={handlePublish} />
        </div>
      </Modal>
    </Main>
  )
}
