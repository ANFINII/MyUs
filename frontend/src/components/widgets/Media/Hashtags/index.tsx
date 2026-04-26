import { ChangeEvent, useState } from 'react'
import { useRouter } from 'next/router'
import { Hashtag } from 'types/internal/media/output'
import { putMediaHashtags } from 'api/internal/hashtag'
import { MediaPath, MediaType } from 'utils/constants/enum'
import ButtonSquare from 'components/parts/Button/Square'
import IconCross from 'components/parts/Icon/Cross'
import IconEdit from 'components/parts/Icon/Edit'
import Input from 'components/parts/Input'
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
  mediaPath: MediaPath
  mediaUlid?: string
  isOwner?: boolean
  onUpdate?: (hashtags: Hashtag[]) => void
  onToast?: (content: string, isError: boolean) => void
}

export default function Hashtags(props: Props): React.JSX.Element {
  const { hashtags, mediaPath, mediaUlid, isOwner = false, onUpdate, onToast } = props
  const router = useRouter()
  const [isEdit, setIsEdit] = useState<boolean>(false)
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [editTags, setEditTags] = useState<Hashtag[]>([])
  const [inputTag, setInputTag] = useState<string>('')

  const canEdit = isOwner && mediaUlid !== undefined

  const handleRouter = (name: string) => {
    router.push(`/media/${mediaPath}?search=${name}`)
  }

  const handleStart = () => {
    setEditTags([...hashtags])
    setInputTag('')
    setIsEdit(true)
  }

  const handleCancel = () => {
    setEditTags([])
    setInputTag('')
    setIsEdit(false)
  }

  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setInputTag(e.target.value)

  const handleAdd = () => {
    const normalized = normalizeName(inputTag)
    if (!isValidName(normalized)) {
      onToast?.('使用できない文字が含まれています', true)
      return
    }
    if (editTags.some((t) => t.name === normalized)) {
      setInputTag('')
      return
    }
    setEditTags([...editTags, { ulid: '', name: normalized }])
    setInputTag('')
  }

  const handleDelete = (index: number) => setEditTags(editTags.filter((_, i) => i !== index))

  const handleSave = async () => {
    if (mediaUlid === undefined) return
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
    onUpdate?.(editTags)
    onToast?.('ハッシュタグを保存しました', false)
    setIsEdit(false)
  }

  if (isEdit) {
    return (
      <VStack gap="2" className={style.edit_area}>
        <HStack gap="2">
          <Input placeholder="タグ名" maxLength={HASHTAG_MAX_LENGTH} value={inputTag} onChange={handleInput} className={style.input} />
          <ButtonSquare name="追加" color="sakura" onClick={handleAdd} />
        </HStack>
        <HStack gap="4" wrap>
          {editTags.map((tag, index) => (
            <span key={tag.name} className={style.edit_chip}>
              <span>#{tag.name}</span>
              <span className={style.delete_button} onClick={() => handleDelete(index)}>
                <IconCross size="14" />
              </span>
            </span>
          ))}
        </HStack>
        <HStack gap="2" className={style.edit_actions}>
          <ButtonSquare name="キャンセル" color="sakura" onClick={handleCancel} />
          <ButtonSquare name="保存" color="emerald" loading={isLoading} onClick={handleSave} />
        </HStack>
      </VStack>
    )
  }

  return (
    <HStack gap="4" wrap>
      {hashtags.map((hashtag) => (
        <span key={hashtag.name} className={style.hashtag} onClick={() => handleRouter(hashtag.name)}>
          #{hashtag.name}
        </span>
      ))}
      {canEdit && (
        <span className={style.edit_button} onClick={handleStart}>
          <IconEdit size="14" />
        </span>
      )}
    </HStack>
  )
}
