import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQueryClient } from '@tanstack/react-query'
import { errorMessage } from 'lib/error'
import { queryKeys } from 'lib/query/keys'
import { Music } from 'types/internal/media/output'
import { Option } from 'types/internal/other'
import { PlaylistDetailOut } from 'types/internal/playlist'
import { deletePlaylist, putPlaylist } from 'api/internal/playlist'
import { Fetch, FetchError } from 'utils/constants/enum'
import cx from 'utils/functions/cx'
import { useDragSort } from 'components/hooks/useDragSort'
import { useLoading } from 'components/hooks/useLoading'
import { useMusicPlayer } from 'components/hooks/useMusicPlayer'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import AvatarLink from 'components/parts/Avatar/Link'
import Button from 'components/parts/Button'
import ExImage from 'components/parts/ExImage'
import IconArrow from 'components/parts/Icon/Arrow'
import IconCross from 'components/parts/Icon/Cross'
import IconGrip from 'components/parts/Icon/Grip'
import IconPlaylist from 'components/parts/Icon/Playlist'
import Input from 'components/parts/Input'
import CheckBox from 'components/parts/Input/CheckBox'
import SelectBox from 'components/parts/Input/SelectBox'
import Textarea from 'components/parts/Input/Textarea'
import Link from 'components/parts/Link'
import HStack from 'components/parts/Stack/Horizontal'
import DeleteModal from 'components/widgets/Modal/Delete'
import ShareButton from 'components/widgets/ShareButton'
import Empty from 'components/widgets/Status/Empty'
import style from './Detail.module.scss'

interface Props {
  data: PlaylistDetailOut
}

export default function PlaylistDetail(props: Props): React.JSX.Element {
  const { data } = props
  const { ulid, title, description, image, thumbnailMusicUlid, publish, isOwner, author, musics } = data

  const router = useRouter()
  const queryClient = useQueryClient()
  const { t } = useTranslation()
  const { current, play, playShuffle } = useMusicPlayer()
  const { loading, handleLoading } = useLoading()
  const { toast, handleToast } = useToast()
  const [isEdit, setIsEdit] = useState<boolean>(false)
  const [isModal, setIsModal] = useState<boolean>(false)
  const [editTitle, setEditTitle] = useState<string>(title)
  const [editDescription, setEditDescription] = useState<string>(description)
  const [editThumbnail, setEditThumbnail] = useState<string>(thumbnailMusicUlid)
  const [isEditPublish, setIsEditPublish] = useState<boolean>(publish)
  const [editMusics, setEditMusics] = useState<Music[]>(musics)
  const { dragIndex, dragOverIndex, dragItem } = useDragSort(editMusics, setEditMusics)

  const editThumbnailMusic = editMusics.find((m) => m.ulid === editThumbnail) ?? editMusics[0]
  const editImage = editThumbnailMusic ? editThumbnailMusic.image || editThumbnailMusic.channel.avatar : ''
  const headerImage = isEdit ? editImage : image
  const thumbnailOptions: Option[] = [{ label: t('playlist.thumbnailAuto'), value: '' }, ...editMusics.map((m) => ({ label: m.title, value: m.ulid }))]

  const handleModal = () => setIsModal(!isModal)
  const handlePlay = (index: number) => play(musics, index)
  const handlePlayShuffle = () => playShuffle(musics)
  const handleStop = (e: React.MouseEvent) => e.stopPropagation()
  const handleTitle = (e: ChangeEvent<HTMLInputElement>) => setEditTitle(e.target.value)
  const handleDescription = (e: ChangeEvent<HTMLTextAreaElement>) => setEditDescription(e.target.value)
  const handleThumbnail = (e: ChangeEvent<HTMLSelectElement>) => setEditThumbnail(e.target.value)
  const handlePublish = (e: ChangeEvent<HTMLInputElement>) => setIsEditPublish(e.target.checked)
  const handleRemove = (index: number) => setEditMusics(editMusics.filter((_, i) => i !== index))

  const handleEdit = () => {
    setEditTitle(title)
    setEditDescription(description)
    setEditThumbnail(thumbnailMusicUlid)
    setIsEditPublish(publish)
    setEditMusics(musics)
    setIsEdit(!isEdit)
  }

  const handleSave = async () => {
    handleLoading(true)
    const thumbnail = editMusics.some((m) => m.ulid === editThumbnail) ? editThumbnail : ''
    const ret = await putPlaylist(ulid, { title: editTitle, description: editDescription, thumbnailMusicUlid: thumbnail, publish: isEditPublish, musicUlids: editMusics.map((m) => m.ulid) })
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
        <div className={style.thumbnail_box}>{headerImage ? <ExImage src={headerImage} className={style.thumbnail} /> : <IconPlaylist size="48" className={style.icon} />}</div>
        <div className={style.info}>
          {isEdit ? (
            <div className={style.form}>
              <Input label={t('playlist.newTitle')} value={editTitle} maxLength={100} onChange={handleTitle} />
              <Textarea label={t('playlist.description')} value={editDescription} onChange={handleDescription} />
              <SelectBox label={t('playlist.thumbnail')} value={editThumbnail} options={thumbnailOptions} onChange={handleThumbnail} />
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
              {description && <p className={style.description}>{description}</p>}
            </div>
          )}
          {!isEdit && (
            <div className={style.actions}>
              <Button name={t('playlist.playAll')} color="blue" size="s" disabled={musics.length === 0} onClick={() => handlePlay(0)} />
              <Button name={t('playlist.playShuffle')} color="purple" size="s" disabled={musics.length === 0} onClick={handlePlayShuffle} />
              {publish && <ShareButton path={`/menu/playlist/${ulid}`} handleToast={handleToast} />}
            </div>
          )}
        </div>
      </section>

      {isEdit ? (
        <ul className={style.list}>
          {editMusics.map((music, index) => (
            <li
              key={music.ulid}
              className={cx(style.item, style.editable, dragIndex === index && style.dragging, dragOverIndex === index && style.drag_over)}
              {...dragItem(index)}
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
              <span className={style.index}>{String(index + 1).padStart(3, '0')}</span>
              <ExImage src={music.image || music.channel.avatar} className={style.item_thumbnail} />
              <div className={style.item_text}>
                <div className={style.item_title}>{music.title}</div>
                <div className={style.item_channel}>{music.channel.name}</div>
              </div>
              <span className={style.detail} onClick={handleStop}>
                <Link href={`/media/music/${music.ulid}`} className={style.detail_link}>
                  <IconArrow size="16" type="external" />
                </Link>
              </span>
            </li>
          ))}
        </ul>
      ) : (
        <Empty content={t('playlist.emptyMusic')} />
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
