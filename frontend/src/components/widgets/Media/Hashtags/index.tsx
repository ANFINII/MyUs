import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useNavigate } from '@tanstack/react-router'
import { HashtagOut } from 'types/internal/hashtag'
import { Hashtag } from 'types/internal/media/output'
import { getHashtags } from 'api/internal/hashtag'
import { MediaPath } from 'utils/constants/enum'
import IconEdit from 'components/parts/Icon/Edit'
import HStack from 'components/parts/Stack/Horizontal'
import HashtagsEdit from './Edit'
import style from './Hashtags.module.scss'

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

  const navigate = useNavigate()
  const { t } = useTranslation()
  const [isEdit, setIsEdit] = useState<boolean>(false)
  const [isMasterLoading, setIsMasterLoading] = useState<boolean>(false)
  const [master, setMaster] = useState<HashtagOut[]>([])

  const canEdit = isOwner && mediaUlid !== undefined

  const handleRouter = (name: string) => {
    navigate({ to: `/media/${mediaPath}` as const, search: { search: name } })
  }

  const handleStart = async () => {
    setIsEdit(true)
    setIsMasterLoading(true)
    const ret = await getHashtags()
    setIsMasterLoading(false)
    if (ret.isErr()) {
      onToast?.(t('hashtag.fetchError'), true)
      return
    }
    setMaster(ret.value)
  }

  const handleCancel = () => setIsEdit(false)

  const handleSave = (saved: Hashtag[]) => {
    onUpdate?.(saved)
    setIsEdit(false)
  }

  if (isEdit && mediaUlid !== undefined) {
    return (
      <HashtagsEdit
        hashtags={hashtags}
        master={master}
        isMasterLoading={isMasterLoading}
        mediaPath={mediaPath}
        mediaUlid={mediaUlid}
        onSave={handleSave}
        onCancel={handleCancel}
        onToast={onToast}
      />
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
