import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQueryClient } from '@tanstack/react-query'
import { errorMessage } from 'lib/error'
import { queryKeys } from 'lib/query/keys'
import { Music } from 'types/internal/media/output'
import { PlaylistDetailOut } from 'types/internal/playlist'
import { deletePlaylist, putPlaylist } from 'api/internal/playlist'
import { Fetch, FetchError } from 'utils/constants/enum'
import cx from 'utils/functions/cx'
import { useLoading } from 'components/hooks/useLoading'
import { useMusicPlayer } from 'components/hooks/useMusicPlayer'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import AvatarLink from 'components/parts/Avatar/Link'
import Button from 'components/parts/Button'
import ExImage from 'components/parts/ExImage'
import IconCross from 'components/parts/Icon/Cross'
import IconGrip from 'components/parts/Icon/Grip'
import IconPlaylist from 'components/parts/Icon/Playlist'
import IconShare from 'components/parts/Icon/Share'
import Input from 'components/parts/Input'
import CheckBox from 'components/parts/Input/CheckBox'
import HStack from 'components/parts/Stack/Horizontal'
import DeleteModal from 'components/widgets/Modal/Delete'
import style from './Detail.module.scss'
import { title } from 'node:process'

interface Props {
  data: PlaylistDetailOut
}

export default function PlaylistDetail(props: Props): React.JSX.Element {
  const { data } = props
  const { ulid, title, publish, isOwner, author, musics } = data

  const router = useRouter()
  const queryClient = useQueryClient()
  const { t } = useTranslation()
  const { current, play, playShuffle } = useMusicPlayer()
  const { loading, handleLoading } = useLoading()
  const { toast, handleToast } = useToast()
  const [isEdit, setIsEdit] = useState<boolean>(false)
  const [isModal, setIsModal] = useState<boolean>(false)
  const [editTitle, setEditTitle] = useState<string>(title)
  const [isEditPublish, setIsEditPublish] = useState<boolean>(publish)
  const [editMusics, setEditMusics] = useState<Music[]>(musics)
  const [dragIndex, setDragIndex] = useState<number | null>(null)
  const [dragOverIndex, setDragOverIndex] = useState<number | null>(null)

  const image = musics[0] ? musics[0].image || musics[0].channel.avatar : ''

  const handleModal = () => setIsModal(!isModal)
  const handlePlay = (index: number) => play(musics, index)
  const handlePlayShuffle = () => playShuffle(musics)
  const handleDetail = (musicUlid: string) => router.push(`/media/music/${musicUlid}`)
  const handleStop = (e: React.MouseEvent) => e.stopPropagation()
  const handleTitle = (e: ChangeEvent<HTMLInputElement>) => setEditTitle(e.target.value)
  const handlePublish = (e: ChangeEvent<HTMLInputElement>) => setIsEditPublish(e.target.checked)
  const handleRemove = (index: number) => setEditMusics(editMusics.filter((_, i) => i !== index))

  const handleShare = async () => {
    try {
      await navigator.clipboard.writeText(router.buildUrl(`/menu/playlist/${ulid}`))
      handleToast('playlist.shareCopied', false)
    } catch {
      handleToast('playlist.shareFailed', true)
    }
  }

  const handleEdit = () => {
    setEditTitle(title)
    setIsEditPublish(publish)
    setEditMusics(musics)
    setIsEdit(!isEdit)
  }

  const handleDragStart = (index: number) => setDragIndex(index)

  const handleDrag = (e: React.DragEvent, index: number | null = null) => {
    e.preventDefault()
    setDragOverIndex(index)
  }

  const handleDrop = (index: number) => {
    if (dragIndex === null || dragIndex === index) return
    const newMusics = [...editMusics]
    const removed = newMusics.splice(dragIndex, 1)
    if (removed[0] === undefined) return
    newMusics.splice(index, 0, removed[0])
    setEditMusics(newMusics)
  }

  const handleDragEnd = () => {
    setDragIndex(null)
    setDragOverIndex(null)
  }

  const handleSave = async () => {
    handleLoading(true)
    const ret = await putPlaylist(ulid, { title: editTitle, publish: isEditPublish, musicUlids: editMusics.map((m) => m.ulid) })
    handleLoading(false)
    if (ret.isErr()) return handleToast(errorMessage(ret.error, FetchError.Put), true)
    await queryClient.invalidateQueries({ queryKey: queryKeys.mediaPlaylists })
    setIsEdit(false)
    handleToast(Fetch.Save, false)
  }

  const handleDelete = async () => {
    handleLoading(true)
    const ret = await deletePlaylist(ulid)
    handleLoading(false)
    if (ret.isErr()) return handleToast(errorMessage(ret.error, FetchError.Delete), true)
    await queryClient.invalidateQueries({ queryKey: queryKeys.mediaPlaylists })
    router.push('/menu/playlist')
  }

  const button = isOwner && (
    <HStack gap="4">
      {isEdit ? (
        <>
          <Button name={t('action.save')} color="green" size="s" loading={loading} disabled={editTitle.trim() === ''} onClick={handleSave} />
          <Button name={t('action.cancel')} color="blue" size="s" disabled={loading} onClick={handleEdit} />
        </>
      ) : (
        <>
          <Button name={t('action.edit')} color="blue" size="s" onClick={handleEdit} />
          <Button name={t('action.delete')} color="red" size="s" onClick={handleModal} />
        </>
      )}
    </HStack>
  )

  return (
    <Main title="Playlist" type="table" toast={toast} button={button}>
      <section className={style.header}>
        <div className={style.thumbnail_box}>{image ? <ExImage src={image} className={style.thumbnail} /> : <IconPlaylist size="48" className={style.icon} />}</div>
        <div className={style.info}>
          {isEdit ? (
            <div className={style.form}>
              <Input label={t('playlist.newTitle')} value={editTitle} maxLength={100} onChange={handleTitle} />
              <CheckBox label={t('playlist.publish')} id="playlist_publish_edit" checked={isEditPublish} onChange={handlePublish} />
            </div>
          ) : (
            <div className={style.heading}>
              <div className={style.meta}>
                <AvatarLink size="s" src={author.avatar} ulid={author.ulid} title={author.nickname} />
                <span>{t('playlist.count', { count: musics.length })}</span>
                <span>{publish ? t('playlist.public') : t('playlist.private')}</span>
              </div>
              <h2 className={style.title}>{title}</h2>
            </div>
          )}
          {!isEdit && (
            <div className={style.actions}>
              <Button name={t('playlist.playAll')} color="blue" size="s" disabled={musics.length === 0} onClick={() => handlePlay(0)} />
              {publish && <Button name={t('playlist.share')} size="s" icon={<IconShare size="14" />} onClick={handleShare} />}
            </div>
          )}
        </div>
      </section>

      {isEdit ? (
        <ul className={style.list}>
          {editMusics.map((music, index) => (
            <li
              key={music.ulid}
              draggable
              className={cx(style.item, style.editable, dragIndex === index && style.dragging, dragOverIndex === index && style.drag_over)}
              onDragStart={() => handleDragStart(index)}
              onDragOver={(e) => handleDrag(e, index)}
              onDragLeave={(e) => handleDrag(e)}
              onDrop={() => handleDrop(index)}
              onDragEnd={handleDragEnd}
            >
              <IconGrip size="14" className={style.grip} />
              <ExImage src={music.image || music.channel.avatar} className={style.item_thumbnail} />
              <div className={style.item_text}>
                <div className={style.item_title}>{music.title}</div>
                <div className={style.item_channel}>{music.channel.name}</div>
              </div>
              <button type="button" title={t('action.delete')} className={style.remove} onClick={() => handleRemove(index)}>
                <IconCross size="18" />
              </button>
            </li>
          ))}
        </ul>
      ) : musics.length > 0 ? (
        <ul className={style.list}>
          {musics.map((music, index) => (
            <li key={music.ulid} className={cx(style.item, current?.ulid === music.ulid && style.current)} onClick={() => handlePlay(index)}>
              <span className={style.index}>{index + 1}</span>
              <ExImage src={music.image || music.channel.avatar} className={style.item_thumbnail} />
              <div className={style.item_text}>
                <div className={style.item_title}>{music.title}</div>
                <div className={style.item_channel}>{music.channel.name}</div>
              </div>
              <span className={style.detail} onClick={handleStop}>
                <Button name={t('playlist.detail')} color="purple" size="s" onClick={() => handleDetail(music.ulid)} />
              </span>
            </li>
          ))}
        </ul>
      ) : (
        <p className={style.empty}>{t('playlist.emptyMusic')}</p>
      )}

      <DeleteModal
        open={isModal}
        title={t('playlist.deleteTitle')}
        content={t('playlist.deleteConfirm', { title })}
        loading={loading}
        onClose={handleModal}
        onAction={handleDelete}
      />
    </Main>
  )
}
