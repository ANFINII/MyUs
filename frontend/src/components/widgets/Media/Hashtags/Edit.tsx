import { ChangeEvent, useState } from 'react'
import { HashtagOut } from 'types/internal/hashtag'
import { Hashtag } from 'types/internal/media/output'
import { putMediaHashtags } from 'api/internal/hashtag'
import { MediaPath, MediaType } from 'utils/constants/enum'
import cx from 'utils/functions/cx'
import Button from 'components/parts/Button'
import IconCross from 'components/parts/Icon/Cross'
import IconGrip from 'components/parts/Icon/Grip'
import Input from 'components/parts/Input'
import Spinner from 'components/parts/Spinner'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import style from './Hashtags.module.scss'

const HASHTAG_MAX_LENGTH = 30
const ALLOWED_PATTERN = /^[ぁ-んァ-ヶー一-龯a-zA-Z]+$/

const pathToTypeMap: Record<MediaPath, MediaType> = {
  [MediaPath.Video]: MediaType.Video,
  [MediaPath.Music]: MediaType.Music,
  [MediaPath.Blog]: MediaType.Blog,
  [MediaPath.Comic]: MediaType.Comic,
  [MediaPath.Picture]: MediaType.Picture,
  [MediaPath.Chat]: MediaType.Chat,
}

const normalizeName = (raw: string): string => raw.trim().replace(/^#+/, '').toLowerCase()
const isValidName = (name: string): boolean => name.length > 0 && name.length <= HASHTAG_MAX_LENGTH && ALLOWED_PATTERN.test(name)

interface Props {
  hashtags: Hashtag[]
  master: HashtagOut[]
  isMasterLoading: boolean
  mediaPath: MediaPath
  mediaUlid: string
  onSave: (hashtags: Hashtag[]) => void
  onCancel: () => void
  onToast?: (content: string, isError: boolean) => void
}

export default function HashtagsEdit(props: Props): React.JSX.Element {
  const { hashtags, master, isMasterLoading, mediaPath, mediaUlid, onSave, onCancel, onToast } = props

  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [editTags, setEditTags] = useState<Hashtag[]>([...hashtags])
  const [inputTag, setInputTag] = useState<string>('')
  const [dragIndex, setDragIndex] = useState<number | null>(null)
  const [dragOverIndex, setDragOverIndex] = useState<number | null>(null)

  const normalizedInput = normalizeName(inputTag)
  const editNames = new Set(editTags.map((t) => t.name))
  const filteredMaster = master.filter((m) => !editNames.has(m.name) && (normalizedInput === '' || m.name.includes(normalizedInput)))
  const showNewRow = isValidName(normalizedInput) && !editNames.has(normalizedInput) && !master.some((m) => m.name === normalizedInput)

  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setInputTag(e.target.value)
  const handleDelete = (index: number) => setEditTags(editTags.filter((_, i) => i !== index))

  const handleAddMaster = (item: HashtagOut) => {
    setEditTags([...editTags, { ulid: item.ulid, name: item.name }])
    setInputTag('')
  }

  const handleAddNew = () => {
    setEditTags([...editTags, { ulid: '', name: normalizedInput }])
    setInputTag('')
  }

  const handleDragStart = (index: number) => setDragIndex(index)

  const handleDrag = (e: React.DragEvent, index: number | null = null) => {
    e.preventDefault()
    setDragOverIndex(index)
  }

  const handleDrop = (index: number) => {
    if (dragIndex === null || dragIndex === index) return
    const newTags = [...editTags]
    const removed = newTags.splice(dragIndex, 1)
    if (removed[0] === undefined) return
    newTags.splice(index, 0, removed[0])
    setEditTags(newTags)
  }

  const handleDragEnd = () => {
    setDragIndex(null)
    setDragOverIndex(null)
  }

  const handleSave = async () => {
    setIsLoading(true)
    const ret = await putMediaHashtags({
      mediaType: pathToTypeMap[mediaPath],
      mediaUlid,
      hashtags: editTags,
    })
    setIsLoading(false)
    if (ret.isErr()) {
      onToast?.('ハッシュタグの保存に失敗しました', true)
      return
    }
    onSave(editTags)
    onToast?.('ハッシュタグを保存しました', false)
  }

  return (
    <VStack gap="2" className={style.edit_area}>
      <Input placeholder="タグ名" maxLength={HASHTAG_MAX_LENGTH} value={inputTag} onChange={handleInput} className={style.input} />
      <VStack gap="1" className={style.master_list}>
        {isMasterLoading ? (
          <HStack justify="center" className={style.loading}>
            <Spinner color="gray" size="s" />
          </HStack>
        ) : (
          <>
            {showNewRow && (
              <HStack gap="2" justify="between" className={style.master_row}>
                <span className={style.master_name}>
                  #{normalizedInput} <span className={style.new_label}>(新規)</span>
                </span>
                <Button size="s" color="blue" name="追加" onClick={handleAddNew} />
              </HStack>
            )}
            {filteredMaster.map((m) => (
              <HStack key={m.ulid} gap="2" justify="between" className={style.master_row}>
                <span className={style.master_name}>#{m.name}</span>
                <Button size="s" color="blue" name="追加" onClick={() => handleAddMaster(m)} />
              </HStack>
            ))}
            {!showNewRow && filteredMaster.length === 0 && <span className={style.empty}>候補なし</span>}
          </>
        )}
      </VStack>
      <HStack gap="4" wrap>
        {editTags.map((tag, index) => (
          <span
            key={tag.name}
            className={cx(style.edit_chip, dragIndex === index && style.dragging, dragOverIndex === index && style.drag_over)}
            draggable
            onDragStart={() => handleDragStart(index)}
            onDragOver={(e) => handleDrag(e, index)}
            onDragLeave={(e) => handleDrag(e)}
            onDrop={() => handleDrop(index)}
            onDragEnd={handleDragEnd}
          >
            <span className={style.drag_handle}>
              <IconGrip size="12" />
            </span>
            <span>#{tag.name}</span>
            <span className={style.delete_button} onClick={() => handleDelete(index)}>
              <IconCross size="14" />
            </span>
          </span>
        ))}
      </HStack>
      <HStack gap="2" className={style.edit_actions}>
        <Button size="s" name="キャンセル" disabled={isLoading} onClick={onCancel} />
        <Button size="s" color="green" name="保存" loading={isLoading} onClick={handleSave} />
      </HStack>
    </VStack>
  )
}
