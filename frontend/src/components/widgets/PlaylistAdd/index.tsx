import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { errorMessage } from 'lib/error'
import { isTranslationKey } from 'lib/i18n'
import { Playlist } from 'types/internal/playlist'
import { getPlaylists, postPlaylist, postPlaylistMusic } from 'api/internal/playlist'
import { FetchError } from 'utils/constants/enum'
import cx from 'utils/functions/cx'
import { useLoading } from 'components/hooks/useLoading'
import { useUser } from 'components/hooks/useUser'
import Button from 'components/parts/Button'
import IconPlus from 'components/parts/Icon/Plus'
import Input from 'components/parts/Input'
import CheckBox from 'components/parts/Input/CheckBox'
import Link from 'components/parts/Link'
import Modal from 'components/parts/Modal'
import style from './PlaylistAdd.module.scss'

interface Props {
  musicUlid: string
  className?: string
}

export default function PlaylistAdd(props: Props): React.JSX.Element {
  const { musicUlid, className } = props

  const { t, i18n } = useTranslation()
  const { user } = useUser()
  const { loading, handleLoading } = useLoading()
  const [isModal, setIsModal] = useState<boolean>(false)
  const [playlists, setPlaylists] = useState<Playlist[]>([])
  const [addedUlids, setAddedUlids] = useState<string[]>([])
  const [addingUlid, setAddingUlid] = useState<string>('')
  const [title, setTitle] = useState<string>('')
  const [isPublish, setIsPublish] = useState<boolean>(false)
  const [error, setError] = useState<string>('')

  const handleError = (content: string) => setError(isTranslationKey(i18n, content) ? t(content) : content)
  const handleTitle = (e: ChangeEvent<HTMLInputElement>) => setTitle(e.target.value)
  const handlePublish = (e: ChangeEvent<HTMLInputElement>) => setIsPublish(e.target.checked)

  const handleModal = async () => {
    if (isModal) return setIsModal(false)
    setError('')
    setAddedUlids([])
    setIsModal(true)
    if (!user.isActive) return
    const ret = await getPlaylists()
    if (ret.isErr()) return handleError(errorMessage(ret.error, FetchError.Get))
    setPlaylists(ret.value.items)
  }

  const handleAdd = async (ulid: string) => {
    setAddingUlid(ulid)
    const ret = await postPlaylistMusic(ulid, { musicUlid })
    setAddingUlid('')
    if (ret.isErr()) return handleError(errorMessage(ret.error, FetchError.Post))
    setAddedUlids((prev) => [...prev, ulid])
  }

  const handleCreate = async () => {
    handleLoading(true)
    const ret = await postPlaylist({ title, publish: isPublish, musicUlid })
    handleLoading(false)
    if (ret.isErr()) return handleError(errorMessage(ret.error, FetchError.Post))
    const playlist: Playlist = { ulid: ret.value.ulid, title, publish: isPublish, count: 1, image: '', updated: '' }
    setPlaylists((prev) => [playlist, ...prev])
    setAddedUlids((prev) => [...prev, playlist.ulid])
    setTitle('')
    setIsPublish(false)
  }

  return (
    <>
      <button type="button" title={t('playlist.add')} className={cx(style.button, className)} onClick={handleModal}>
        <IconPlus size="1.25em" />
      </button>

      <Modal open={isModal} onClose={handleModal} title={t('playlist.add')} size="s">
        {user.isActive ? (
          <div className={style.content}>
            {playlists.length > 0 ? (
              <ul className={style.list}>
                {playlists.map((playlist) => (
                  <li key={playlist.ulid} className={style.item}>
                    <span className={style.title}>{playlist.title}</span>
                    <span className={style.publish}>{playlist.publish ? t('playlist.public') : t('playlist.private')}</span>
                    <Button
                      name={addedUlids.includes(playlist.ulid) ? t('playlist.added') : t('action.add')}
                      color="blue"
                      size="s"
                      loading={addingUlid === playlist.ulid}
                      disabled={addedUlids.includes(playlist.ulid)}
                      onClick={() => handleAdd(playlist.ulid)}
                    />
                  </li>
                ))}
              </ul>
            ) : (
              <p className={style.empty}>{t('playlist.empty')}</p>
            )}
            <div className={style.create}>
              <Input label={t('playlist.newTitle')} value={title} maxLength={100} onChange={handleTitle} />
              <div className={style.create_actions}>
                <CheckBox label={t('playlist.publish')} id={`playlist_publish_${musicUlid}`} checked={isPublish} onChange={handlePublish} />
                <Button name={t('playlist.create')} color="green" size="s" loading={loading} disabled={title.trim() === ''} onClick={handleCreate} />
              </div>
            </div>
            {error && <p className={style.error}>{error}</p>}
          </div>
        ) : (
          <div className={style.content}>
            <p>{t('playlist.loginRequired')}</p>
            <Link href="/account/login" className={style.login}>
              {t('playlist.login')}
            </Link>
          </div>
        )}
      </Modal>
    </>
  )
}
