import { useRef, useState, useEffect, ChangeEvent } from 'react'
import Link from 'next/link'
import { SearchTagOut } from 'types/internal/user'
import { getSearchTag, putSearchTag } from 'api/internal/user'
import cx from 'utils/functions/cx'
import { useUser } from 'components/hooks/useUser'
import ButtonSquare from 'components/parts/Button/Square'
import IconChevront from 'components/parts/Icon/Chevront'
import IconCross from 'components/parts/Icon/Cross'
import IconGrip from 'components/parts/Icon/Grip'
import Input from 'components/parts/Input'
import HStack from 'components/parts/Stack/Horizontal'
import styles from './SearchTagBar.module.scss'

export default function SearchTagBar(): React.JSX.Element {
  const { user } = useUser()
  const scrollRef = useRef<HTMLDivElement>(null)
  const [isILoading, setILoading] = useState<boolean>(false)
  const [isSearchtag, setIsSearchtag] = useState<boolean>(false)
  const [inputTag, setInputTag] = useState<string>('')
  const [searchTags, setSearchTags] = useState<SearchTagOut[]>([])
  const [editTags, setEditTags] = useState<SearchTagOut[]>([])
  const [dragIndex, setDragIndex] = useState<number | null>(null)
  const [dragOverIndex, setDragOverIndex] = useState<number | null>(null)

  useEffect(() => {
    const fetchSearchTag = async () => {
      const ret = await getSearchTag()
      if (ret.isErr()) return
      const data = ret.value
      const sortedData = data.sort((a: SearchTagOut, b: SearchTagOut) => a.sequence - b.sequence)
      setSearchTags(sortedData)
    }
    if (user.isActive) {
      fetchSearchTag()
    } else {
      setSearchTags([])
    }
  }, [user])

  const hasChanges = () => {
    if (editTags.length !== searchTags.length) return true
    return editTags.some((tag, i) => tag.name !== searchTags[i]?.name)
  }

  const handleSearchtag = async () => {
    if (isSearchtag) {
      if (hasChanges()) {
        setILoading(true)
        const tags = editTags.map((tag, i) => ({ sequence: i + 1, name: tag.name }))
        const ret = await putSearchTag(tags)
        if (ret.isOk()) {
          setSearchTags(tags)
        }
        setILoading(false)
      }
      setIsSearchtag(false)
    } else {
      setEditTags([...searchTags])
      setInputTag('')
      setIsSearchtag(true)
    }
  }

  const handleAdd = () => {
    const name = inputTag.trim()
    if (name === '') return
    const isDuplicate = editTags.some((tag) => tag.name === name)
    if (isDuplicate) return
    setEditTags([...editTags, { sequence: editTags.length + 1, name }])
    setInputTag('')
  }

  const handleDelete = (index: number) => setEditTags(editTags.filter((_, i) => i !== index))
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setInputTag(e.target.value)
  const handleDragStart = (index: number) => setDragIndex(index)

  const handleDrop = (index: number) => {
    if (dragIndex === null || dragIndex === index) return
    const newTags = [...editTags]
    const removed = newTags.splice(dragIndex, 1)
    if (removed[0] === undefined) return
    newTags.splice(index, 0, removed[0])
    setEditTags(newTags)
  }

  const handleDrag = (e: React.DragEvent, index: number | null = null) => {
    e.preventDefault()
    setDragOverIndex(index)
  }

  const handleDragEnd = () => {
    setDragIndex(null)
    setDragOverIndex(null)
  }

  const handleScroll = (direction: number) => {
    if (scrollRef.current) {
      scrollRef.current.scrollLeft += direction
    }
  }

  return (
    <nav className={styles.searchtag}>
      <HStack justify="between">
        <HStack gap="3">
          <HStack gap="0.5">
            <ButtonSquare color="emerald" name={isSearchtag ? '完了' : 'タグ'} loading={isILoading} onClick={handleSearchtag} />
            <Input
              placeholder="タグ名"
              maxLength={30}
              value={inputTag}
              disabled={!user.isActive}
              className={cx(styles.input, isSearchtag && styles.active)}
              onChange={handleInput}
            />
            <ButtonSquare color="sakura" name="追加" className={cx(styles.button, isSearchtag && styles.active)} onClick={handleAdd} />
          </HStack>
          <div ref={scrollRef} className={cx(styles.tags, isSearchtag && styles.active)}>
            <HStack gap="2.5">
              {isSearchtag
                ? editTags.map((tag, index) => (
                    <div
                      key={tag.name}
                      className={cx(styles.tag_item, dragIndex === index && styles.dragging, dragOverIndex === index && styles.drag_over)}
                      draggable
                      onDragStart={() => handleDragStart(index)}
                      onDragOver={(e) => handleDrag(e, index)}
                      onDragLeave={(e) => handleDrag(e)}
                      onDrop={() => handleDrop(index)}
                      onDragEnd={handleDragEnd}
                    >
                      <span className={styles.drag_handle}>
                        <IconGrip size="12" />
                      </span>
                      <span className={styles.tag_name}>{tag.name}</span>
                      <span className={styles.delete_button} onClick={() => handleDelete(index)}>
                        <IconCross size="18" />
                      </span>
                    </div>
                  ))
                : searchTags.map((tag) => (
                    <Link key={tag.sequence} href={`?search=${tag.name}`}>
                      {tag.name}
                    </Link>
                  ))}
            </HStack>
          </div>
        </HStack>
        <HStack>
          <div className={styles.arrow} onClick={() => handleScroll(-200)}>
            <IconChevront width="18" height="17" type="left" />
          </div>
          <div className={styles.arrow} onClick={() => handleScroll(200)}>
            <IconChevront width="18" height="17" type="right" />
          </div>
        </HStack>
      </HStack>
    </nav>
  )
}
