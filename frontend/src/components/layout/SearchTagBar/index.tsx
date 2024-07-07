import { useState, useRef, useEffect } from 'react'
import Link from 'next/link'
import clsx from 'clsx'
import { getSearchTag } from 'api/user'
import { SearchTagOut } from 'types/internal/auth'
import ButtonSquare from 'components/parts/Button/Square'
import IconChevront from 'components/parts/Icon/Chevront'
import Input from 'components/parts/Input'

interface Props {
  isAuth: boolean
  csrfToken?: string
}

export default function SearchTagBar(props: Props) {
  const { isAuth, csrfToken } = props

  const scrollRef = useRef<HTMLDivElement>(null)
  const [isSearchtag, setIsSearchtag] = useState(false)
  const [scrollPosition, setScrollPosition] = useState(0)
  const [searchTags, setSearchTags] = useState<SearchTagOut[]>([])

  useEffect(() => {
    const fetchSearchTag = async (): Promise<void> => {
      const data = await getSearchTag()
      const sortedData = data.sort((a, b) => a.sequence - b.sequence)
      setSearchTags(sortedData)
    }
    fetchSearchTag()
  }, [])

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
        <ButtonSquare color="emerald" name="タグ" className={clsx('searchtag_1', isSearchtag ? 'active' : '')} onClick={handleSearchtag} />

        <ButtonSquare color="sakura" name="追加" className={clsx('searchtag_2', isSearchtag ? 'active' : '')} data-csrf={csrfToken} />

        <Input name="searchtag" className={clsx('searchtag_3', isSearchtag ? 'active' : '')} maxLength={30} placeholder="タグ名" disabled={isAuth} />
        <div className={isSearchtag ? 'searchtag_n active' : 'searchtag_n'} ref={scrollRef}>
          <div className="searchtag_n_list">
            {searchTags?.map((tag, index) => (
              <Link href={`?search=${tag.name}`} data-search={tag.name} key={index}>
                {tag.name}
              </Link>
            ))}
          </div>
        </div>

        <ButtonSquare color="emerald" name="完了" className={clsx('searchtag_4', isSearchtag ? 'active' : '')} onClick={handleSearchtag} data-csrf={csrfToken} />

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
