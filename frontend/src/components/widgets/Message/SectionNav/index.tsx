import { MouseEvent, RefObject } from 'react'
import Link from 'next/link'
import { Chat } from 'types/internal/media'
import Avatar from 'components/parts/Avatar'
import IconResize from 'components/parts/Icon/Resize'
import style from './SectionNav.module.scss'

interface Props {
  navRef: RefObject<HTMLDivElement | null>
  list: Chat[]
  onNav: () => void
  onResize: (e: MouseEvent) => void
}

export default function SectionNav(props: Props): React.JSX.Element {
  const { navRef, list, onNav, onResize } = props

  return (
    <div ref={navRef} className={style.chat_section_nav}>
      <div className={style.nav_toggle} onClick={onNav}>
        <IconResize size="15" />
      </div>
      <div className={style.nav_area}>
        {list.map((item) => (
          <div key={item.ulid} className={style.nav_item}>
            <Avatar src={item.channel.avatar} size="40" />
            <Link href={`/media/chat/${item.ulid}`}>
              <h3 className={style.nav_title} title={item.title}>
                {item.title}
              </h3>
            </Link>
          </div>
        ))}
      </div>
      <div className={style.nav_resize} onMouseDown={onResize} />
    </div>
  )
}
