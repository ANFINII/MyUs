import Link from 'next/link'
import { useRouter } from 'next/router'
import IconBlog from 'components/parts/Icon/Blog'
import IconChat from 'components/parts/Icon/Chat'
import IconComic from 'components/parts/Icon/Comic'
import IconMusic from 'components/parts/Icon/Music'
import IconPicture from 'components/parts/Icon/Picture'
import IconVideo from 'components/parts/Icon/Video'

export default function SideBar() {
  const router = useRouter()

  return (
    <aside className="sidebar">
      <nav className="sidebar_nav">
        <ul>
          <li className={'sidebar_color' + (router.pathname === '/media/video' ? ' ' + 'active' : '')}>
            <Link href="/media/video" className="pjax_button">
              <IconVideo />
              <p className="sidebar_text">Video</p>
            </Link>
          </li>

          <li className={'sidebar_color' + (router.pathname === '/media/music' ? ' ' + 'active' : '')}>
            <Link href="/media/music" className="pjax_button">
              <IconMusic />
              <p className="sidebar_text">Music</p>
            </Link>
          </li>

          <li className={'sidebar_color' + (router.pathname === '/media/comic' ? ' ' + 'active' : '')}>
            <Link href="/media/comic" className="pjax_button">
              <IconComic />
              <p className="sidebar_text">Comic</p>
            </Link>
          </li>

          <li className={'sidebar_color' + (router.pathname === '/media/picture' ? ' ' + 'active' : '')}>
            <Link href="/media/picture" className="pjax_button">
              <IconPicture />
              <p className="sidebar_text">Picture</p>
            </Link>
          </li>

          <li className={'sidebar_color' + (router.pathname === '/media/blog' ? ' ' + 'active' : '')}>
            <Link href="/media/blog" className="pjax_button">
              <IconBlog />
              <p className="sidebar_text">Blog</p>
            </Link>
          </li>

          <li className={'sidebar_color' + (router.pathname === '/media/chat' ? ' ' + 'active' : '')}>
            <Link href="/media/chat" className="pjax_button">
              <IconChat />
              <p className="sidebar_text">Chat</p>
            </Link>
          </li>
        </ul>
      </nav>
    </aside>
  )
}
