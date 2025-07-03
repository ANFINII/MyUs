import { useRef, useState, useEffect } from 'react'
import Link from 'next/link'
import clsx from 'clsx'
import { SearchTagOut } from 'types/internal/auth'
import { getSearchTag } from 'api/internal/user'
import { isActive } from 'utils/functions/common'
import { useUser } from 'components/hooks/useUser'
import ButtonSquare from 'components/parts/Button/Square'
import IconChevront from 'components/parts/Icon/Chevront'
import Input from 'components/parts/Input'
import HStack from 'components/parts/Stack/Horizontal'

export default function SearchTagBar(): JSX.Element {
  const { user } = useUser()
  const scrollRef = useRef<HTMLDivElement>(null)
  const [isSearchtag, setIsSearchtag] = useState(false)
  const [scrollPosition, setScrollPosition] = useState(0)
  const [searchTags, setSearchTags] = useState<SearchTagOut[]>([])

  useEffect(() => {
    const fetchSearchTag = async (): Promise<void> => {
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

  const handleSearchtag = () => setIsSearchtag(!isSearchtag)

  const handleLeft = () => {
    const scrollContainer = scrollRef.current
    if (scrollContainer) {
      scrollContainer.scrollLeft -= 200
      setScrollPosition(scrollPosition)
    }
  }

  const handleRight = () => {
    const scrollContainer = scrollRef.current
    if (scrollContainer) {
      scrollContainer.scrollLeft += 200
      setScrollPosition(scrollPosition)
    }
  }

  return (
    <nav className="searchtag">
      <HStack justify="between">
        <HStack gap="3">
          <HStack gap="0.5">
            <ButtonSquare color="emerald" name={isSearchtag ? '完了' : 'タグ'} className="button_1" onClick={handleSearchtag} />
            <Input placeholder="タグ名" maxLength={30} disabled={!user.isActive} className={clsx('input', isActive(isSearchtag))} />
            <ButtonSquare color="sakura" name="追加" className={clsx('button_2', isActive(isSearchtag))} />
          </HStack>
          <div ref={scrollRef} className={clsx('tags', isActive(isSearchtag))}>
            <HStack gap="2.5">
              {searchTags?.map((tag) => (
                <Link key={tag.sequence} href={`?search=${tag.name}`}>
                  {tag.name}
                </Link>
              ))}
            </HStack>
          </div>
        </HStack>
        <HStack>
          <div className="arrow" onClick={handleLeft}>
            <IconChevront width="18" height="17" type="left" />
          </div>
          <div className="arrow" onClick={handleRight}>
            <IconChevront width="18" height="17" type="right" />
          </div>
        </HStack>
      </HStack>
    </nav>
  )
}
