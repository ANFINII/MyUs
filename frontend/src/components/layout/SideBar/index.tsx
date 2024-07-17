import Link from 'next/link'
import { useRouter } from 'next/router'
import clsx from 'clsx'
import { isActive } from 'utils/functions/common'
import IconBlog from 'components/parts/Icon/Blog'
import IconChat from 'components/parts/Icon/Chat'
import IconComic from 'components/parts/Icon/Comic'
import IconMusic from 'components/parts/Icon/Music'
import IconPicture from 'components/parts/Icon/Picture'
import IconVideo from 'components/parts/Icon/Video'

export default function SideBar() {
  const router = useRouter()

  const activeCheck = (url: string) => isActive(router.pathname === url)

  return (
    <aside className="sidebar">
      <nav className="sidebar_nav">
        <ul>
          <li className={clsx('sidebar_color', activeCheck('/media/video'))}>
            <Link href="/media/video">
              <IconVideo size="1.8em" />
              <p className="sidebar_text">Video</p>
            </Link>
          </li>

          <li className={clsx('sidebar_color', activeCheck('/media/music'))}>
            <Link href="/media/music">
              <IconMusic size="1.8em" />
              <p className="sidebar_text">Music</p>
            </Link>
          </li>

          <li className={clsx('sidebar_color', activeCheck('/media/comic'))}>
            <Link href="/media/comic">
              <IconComic size="1.8em" />
              <p className="sidebar_text">Comic</p>
            </Link>
          </li>

          <li className={clsx('sidebar_color', activeCheck('/media/picture'))}>
            <Link href="/media/picture">
              <IconPicture size="1.8em" />
              <p className="sidebar_text">Picture</p>
            </Link>
          </li>

          <li className={clsx('sidebar_color', activeCheck('/media/blog'))}>
            <Link href="/media/blog">
              <IconBlog size="1.8em" />
              <p className="sidebar_text">Blog</p>
            </Link>
          </li>

          <li className={clsx('sidebar_color', activeCheck('/media/chat'))}>
            <Link href="/media/chat">
              <IconChat size="1.8em" />
              <p className="sidebar_text">Chat</p>
            </Link>
          </li>
        </ul>
      </nav>
    </aside>
  )
}
