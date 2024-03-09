import { useState, useRef } from 'react'
import Link from 'next/link'
import clsx from 'clsx'
import ButtonSquare from 'components/parts/Button/Square'
import Input from 'components/parts/Input'

interface searchtag {
  name: string
}

interface Props {
  isAuth: boolean
  csrfToken?: string
  searchtags?: searchtag[]
}

export default function SearchTagBar(props: Props) {
  const { isAuth, csrfToken, searchtags } = props

  const scrollRef = useRef<HTMLDivElement>(null)
  const [isSearchtag, setIsSearchtag] = useState(false)
  const [scrollPosition, setScrollPosition] = useState(0)

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
            {searchtags?.map((tag: searchtag, index) => {
              return (
                <Link href={`?search=${tag.name}`} data-search={tag.name} key={index}>
                  {tag.name}
                </Link>
              )
            })}
          </div>
        </div>

        <ButtonSquare color="emerald" name="完了" className={isSearchtag ? 'searchtag_4 active' : 'searchtag_4'} onClick={handleSearchtag} data-csrf={csrfToken} />

        <div className="searchtag_left" onClick={handleLeft}>
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="17" fill="currentColor" className="bi-chevron-left" viewBox="0 0 16 16">
            <path fillRule="evenodd" d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z" />
          </svg>
        </div>
        <div className="searchtag_right" onClick={handleRight}>
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="17" fill="currentColor" className="bi-chevron-right" viewBox="0 0 16 16">
            <path fillRule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z" />
          </svg>
        </div>
      </form>
    </nav>
  )
}
