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
      <form method="POST" action="" className="searchtag_grid">
        <ButtonSquare color="emerald" name="タグ" className={clsx('searchtag_1', isActive(isSearchtag))} onClick={handleSearchtag} />

        <ButtonSquare color="sakura" name="追加" className={clsx('searchtag_2', isActive(isSearchtag))} />

        <Input placeholder="タグ名" maxLength={30} disabled={!user.isActive} className={clsx('searchtag_3', isActive(isSearchtag))} />
        <div ref={scrollRef} className={clsx('searchtag_n', isActive(isSearchtag))}>
          <div className="searchtag_n_list">
            {searchTags?.map((tag) => (
              <Link key={tag.sequence} href={`?search=${tag.name}`}>
                {tag.name}
              </Link>
            ))}
          </div>
        </div>

        <ButtonSquare color="emerald" name="完了" className={clsx('searchtag_4', isActive(isSearchtag))} onClick={handleSearchtag} />

        <div className="searchtag_left" onClick={handleLeft}>
          <IconChevront width="18" height="17" type="left" />
        </div>

        <div className="searchtag_right" onClick={handleRight}>
          <IconChevront width="18" height="17" type="right" />
        </div>
      </form>
    </nav>
  )
}
