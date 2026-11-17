import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { errorMessage } from 'lib/error'
import { isTranslationKey } from 'lib/i18n'
import { Playlist } from 'types/internal/playlist'
import { deletePlaylistMusic, getPlaylists, postPlaylist, postPlaylistMusic } from 'api/internal/playlist'
import { FetchError } from 'utils/constants/enum'
import cx from 'utils/functions/cx'
import { useLoading } from 'components/hooks/useLoading'
import { useUser } from 'components/hooks/useUser'
import Button from 'components/parts/Button'
import IconPlus from 'components/parts/Icon/Plus'
import Input from 'components/parts/Input'
import CheckBox from 'components/parts/Input/CheckBox'
import SelectBox from 'components/parts/Input/SelectBox'
import Modal from 'components/parts/Modal'
import LoginRequired from 'components/widgets/Status/LoginRequired'
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
  const [isSaving, setIsSaving] = useState<boolean>(false)
  const [isPublish, setIsPublish] = useState<boolean>(false)
  const [title, setTitle] = useState<string>('')
  const [error, setError] = useState<string>('')
  const [selectedUlid, setSelectedUlid] = useState<string>('')
  const [playlists, setPlaylists] = useState<Playlist[]>([])

  const selected = playlists.find((p) => p.ulid === selectedUlid)
  const isAdded = selected?.musicUlids.includes(musicUlid) ?? false
  const options = playlists.map((p) => ({ label: p.title, value: p.ulid }))

  const handleError = (content: string) => setError(isTranslationKey(i18n, content) ? t(content) : content)
  const handleTitle = (e: ChangeEvent<HTMLInputElement>) => setTitle(e.target.value)
  const handlePublish = (e: ChangeEvent<HTMLInputElement>) => setIsPublish(e.target.checked)
  const handleSelect = (e: ChangeEvent<HTMLSelectElement>) => setSelectedUlid(e.target.value)

  const handleModal = async () => {
    if (isModal) return setIsModal(false)
    setError('')
    setIsModal(true)
    if (!user.isActive) return
    const ret = await getPlaylists()
    if (ret.isErr()) return handleError(errorMessage(ret.error, FetchError.Get))
    const items = ret.value.items
    setPlaylists(items)
    setSelectedUlid((items.find((p) => !p.musicUlids.includes(musicUlid)) ?? items[0])?.ulid ?? '')
  }

  const handleAdd = async () => {
    setIsSaving(true)
    const ret = await postPlaylistMusic(selectedUlid, { musicUlid })
    setIsSaving(false)
    if (ret.isErr()) return handleError(errorMessage(ret.error, FetchError.Post))
    setPlaylists((prev) => prev.map((p) => (p.ulid === selectedUlid ? { ...p, count: p.count + 1, musicUlids: [...p.musicUlids, musicUlid] } : p)))
  }

  const handleRemove = async () => {
    setIsSaving(true)
    const ret = await deletePlaylistMusic(selectedUlid, musicUlid)
    setIsSaving(false)
    if (ret.isErr()) return handleError(errorMessage(ret.error, FetchError.Delete))
    setPlaylists((prev) => prev.map((p) => (p.ulid === selectedUlid ? { ...p, count: p.count - 1, musicUlids: p.musicUlids.filter((u) => u !== musicUlid) } : p)))
  }

  const handleCreate = async () => {
    handleLoading(true)
    const ret = await postPlaylist({ title, publish: isPublish, musicUlid })
    handleLoading(false)
    if (ret.isErr()) return handleError(errorMessage(ret.error, FetchError.Post))
    const playlist: Playlist = { ulid: ret.value.ulid, title, publish: isPublish, count: 1, image: '', musicUlids: [musicUlid], updated: '' }
    setPlaylists((prev) => [playlist, ...prev])
    setSelectedUlid(playlist.ulid)
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
              <div className={style.select}>
                <SelectBox label={t('playlist.select')} value={selectedUlid} options={options} className={style.select_box} onChange={handleSelect} />
                {isAdded ? (
                  <Button name={t('action.delete')} color="red" size="s" loading={isSaving} className={style.add} onClick={handleRemove} />
                ) : (
                  <Button name={t('action.add')} color="blue" size="s" loading={isSaving} className={style.add} onClick={handleAdd} />
                )}
              </div>
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
          <LoginRequired className={style.login_required} />
        )}
      </Modal>
    </>
  )
}
